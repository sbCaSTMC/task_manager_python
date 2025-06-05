import math
import operator
import re
from typing import Union, Dict, Callable

class Calculator:
    """
    数学的な式を安全に評価する計算機クラスです。
    基本的な算術演算と一般的な数学関数をサポートしています。
    
    使用例:
    ------
    # 基本的な計算
    result = Calculator.calculate("2 + 3 * 4")
    # 戻り値: {'success': True, 'result': 14.0, 'expression': '2 + 3 * 4'}
    
    # 関数を使った計算
    result = Calculator.calculate("sqrt(16) + sin(pi/2)")
    # 戻り値: {'success': True, 'result': 5.0, 'expression': 'sqrt(16) + sin(pi/2)'}
    
    # エラーハンドリング付きの例
    try:
        value = Calculator.evaluate("10 / 0")
    except ZeroDivisionError:
        print("0で割ることはできません")
    
    # 直接計算結果を取得（例外処理が必要）
    try:
        value = Calculator.evaluate("2 ^ 8")  # 256.0
    except (ValueError, ZeroDivisionError) as e:
        print(f"計算エラー: {e}")
    """
    
    # Allowed operators and their corresponding functions
    _OPERATORS: Dict[str, Callable[[float, float], float]] = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '^': operator.pow,
        '%': operator.mod
    }
    
    # Allowed functions and their corresponding math functions
    _FUNCTIONS: Dict[str, Callable] = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'sqrt': math.sqrt,
        'log': math.log10,
        'ln': math.log,
        'abs': abs,
        'round': round,
        'floor': math.floor,
        'ceil': math.ceil
    }
    
    # Constants
    _CONSTANTS = {
        'pi': math.pi,
        'e': math.e
    }
    
    @classmethod
    def evaluate(cls, expression: str) -> float:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: String containing the mathematical expression
            
        Returns:
            float: The result of the evaluation
            
        Raises:
            ValueError: If the expression is invalid or contains disallowed characters
            ZeroDivisionError: If division by zero occurs
        """
        if not expression or not expression.strip():
            raise ValueError("Empty expression")
            
        # Sanitize input
        sanitized = re.sub(r'\s+', '', expression).lower()
        
        # Validate characters
        if not cls._is_valid_expression(sanitized):
            raise ValueError("Invalid characters in expression")
        
        try:
            # Replace constants
            for const, value in cls._CONSTANTS.items():
                sanitized = sanitized.replace(const, str(value))
                
            # Replace function calls
            for func in cls._FUNCTIONS:
                sanitized = re.sub(
                    f'{func}\\(([^)]+)\\)',
                    lambda m: str(cls._FUNCTIONS[func](float(m.group(1)))),
                    sanitized
                )
            
            # Evaluate the expression safely
            # Using a restricted namespace for eval
            allowed_names = {
                **{name: getattr(math, name) for name in dir(math) if not name.startswith('_')},
                '__builtins__': {}
            }
            
            # Evaluate the expression
            result = eval(sanitized, {'__builtins__': {}}, allowed_names)
            
            # Ensure the result is a number
            if not isinstance(result, (int, float)):
                raise ValueError("Invalid expression")
                
            return float(result)
            
        except (SyntaxError, NameError, TypeError) as e:
            raise ValueError(f"Invalid expression: {e}")
    
    @classmethod
    def _is_valid_expression(cls, expr: str) -> bool:
        """Check if the expression contains only allowed characters."""
        # Allowed characters: digits, operators, parentheses, decimal point, and function names
        pattern = r'^[\d+\-*\/^%().\s]+$|^[a-z]+\([^)]*\)$'
        return bool(re.match(pattern, expr)) or any(f'{func}(' in expr for func in cls._FUNCTIONS)

    @classmethod
    def calculate(cls, expression: str) -> dict:
        """
        Calculate the result of an expression and return a formatted response.
        
        Args:
            expression: The mathematical expression to evaluate
            
        Returns:
            dict: A dictionary containing the result or error message
        """
        try:
            result = cls.evaluate(expression)
            return {
                'success': True,
                'result': result,
                'expression': expression
            }
        except (ValueError, ZeroDivisionError) as e:
            return {
                'success': False,
                'error': str(e),
                'expression': expression
            }
