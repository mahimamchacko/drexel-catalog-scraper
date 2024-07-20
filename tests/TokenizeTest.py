import unittest
from builders.ModelBuilder import build_token
from builders.RequisiteBuilder import tokenize
from models.TokenType import TokenType

class TokenizeTest(unittest.TestCase):
    def test_one_course(self):
        requisite = "CS 260"
        tokens = [
            build_token("CS 260", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_with_grade(self):
        requisite = "CS 260 [Min Grade: C]"
        tokens = [
            build_token("CS 260", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_with_concurrency(self):
        requisite = "CS 260 (Can be taken Concurrently)"
        tokens = [
            build_token("CS 260", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_with_grade_and_concurrency(self):
        requisite = "CHEM 163 [Min Grade: D] (Can be taken Concurrently)"
        tokens = [
            build_token("CHEM 163", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))

    def test_two_courses_and_operation(self):
        requisite = "CHEM 161 [Min Grade: D] and CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("CHEM 161", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_two_courses_or_operation(self):
        requisite = "CHEM 161 [Min Grade: D] or CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("CHEM 161", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_two_nest_courses_or_operation(self):
        requisite = "(PHYS 113 [Min Grade: D] or PHYS 101 [Min Grade: D]) or (CS 171 [Min Grade: D] or CS 143 [Min Grade: D] or ENGR 131 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 113", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CS 171", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("CS 143", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("ENGR 131", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_two_nest_courses_and_operation(self):
        requisite = "(PHYS 113 [Min Grade: D] or PHYS 101 [Min Grade: D]) and (CS 171 [Min Grade: D] or CS 143 [Min Grade: D] or ENGR 131 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 113", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CS 171", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("CS 143", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("ENGR 131", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_one_nest_course_start_asymmetrical_or_operation(self):
        requisite = "CHEM 246 [Min Grade: D] or (CHEM 241 [Min Grade: D] and CHEM 244 [Min Grade: D])"
        tokens = [
            build_token("CHEM 246", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 241", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 244", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_one_nest_course_end_asymmetrical_or_operation(self):
        requisite = "(CHEM 241 [Min Grade: D] and CHEM 244 [Min Grade: D]) or CHEM 246 [Min Grade: D]"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 241", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 244", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("CHEM 246", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))

    def test_one_course_and_one_nest_course_start_asymmetrical_and_operation(self):
        requisite = "CHEM 101 [Min Grade: D] and (CHEM 111 [Min Grade: D] and CHEM 113 [Min Grade: D])"
        tokens = [
            build_token("CHEM 101", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 111", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 113", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_one_nest_course_end_asymmetrical_and_operation(self):
        requisite = "(CHEM 111 [Min Grade: D] and CHEM 113 [Min Grade: D]) and CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 111", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 113", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_two_nest_courses_middle_or_and_operation(self):
        requisite = "(PHYS 153 [Min Grade: D] or PHYS 101 [Min Grade: D]) or MATH 110 [Min Grade: C] and (MATH 121 [Min Grade: C] or MATH 101 [Min Grade: C])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 153", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("MATH 110", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("MATH 121", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("MATH 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_two_nest_courses_middle_and_or_operation(self):
        requisite = "(PHYS 153 [Min Grade: D] or PHYS 101 [Min Grade: D]) and MATH 110 [Min Grade: C] or (MATH 121 [Min Grade: C] or MATH 101 [Min Grade: C])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 153", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("MATH 110", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("MATH 121", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("MATH 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_two_nest_courses_middle_and_and_operation(self):
        requisite = "(PHYS 154 [Min Grade: D] or PHYS 102 [Min Grade: D]) and MATH 122 [Min Grade: D] and (MET 101 [Min Grade: D] or ENGR 220 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 154", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 102", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("MATH 122", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("MET 101", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("ENGR 220", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_one_course_and_two_nest_courses_middle_or_or_operation(self):
        requisite = "(PHYS 154 [Min Grade: D] or PHYS 102 [Min Grade: D]) or MATH 122 [Min Grade: D] or (MET 101 [Min Grade: D] or ENGR 220 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 154", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 102", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("MATH 122", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("MET 101", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("ENGR 220", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_start_or_operation(self):
        requisite = "or BIO 122 [Min Grade: D] or BIO 141 [Min Grade: D] or BIO 131 [Min Grade: D]"
        tokens = [
            build_token("or", TokenType.OrOperation),
            build_token("BIO 122", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("BIO 141", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("BIO 131", TokenType.Course)
        ]
        self.assertEqual(tokens, tokenize(requisite))
    
    def test_start_and_operation(self):
        requisite = "and BIO 122 [Min Grade: D] and BIO 141 [Min Grade: D] and BIO 131 [Min Grade: D]"
        tokens = [
            build_token("and", TokenType.OrOperation),
            build_token("BIO 122", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("BIO 141", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("BIO 131", TokenType.Course)
        ]
        self.assertEqual(tokens, tokenize(requisite))

if __name__ == "__main__":
    unittest.main()