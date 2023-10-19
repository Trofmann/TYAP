from lexical_analysis import LexicalAnalyzer
from syntactical_analysis import SyntacticalAnalyzer

lexical_analyzer = LexicalAnalyzer()
lexical_analyzer.analyze()
lexical_analyzer.write()

syntactical_analyzer = SyntacticalAnalyzer(lexical_analyzer.tokens)
syntactical_analyzer.analyze()
# # Временное решение
# try:
#     syntactical_analyzer.analyze()
# except Exception:
#     pass

syntactical_analyzer.write()
