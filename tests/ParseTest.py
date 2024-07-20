import unittest
from builders.ModelBuilder import build_requisite, build_tag, build_token
from builders.RequisiteBuilder import parse
from models.TokenType import TokenType

class ParseTest(unittest.TestCase):
    def test_one_course(self):
        data = "CS 260"
        tokens = [
            build_token("CS 260", TokenType.Course),
        ]
        requisite = build_tag("CS", "260")
        self.assertEqual(requisite, parse(tokens))

    def test_two_courses_and_operation(self):
        data = "CHEM 161 [Min Grade: D] and CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("CHEM 161", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        requisite = build_requisite("and")
        requisite.add_tag(build_tag("CHEM", "161"))
        requisite.add_tag(build_tag("CHEM", "101"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_two_courses_or_operation(self):
        data = "CHEM 161 [Min Grade: D] or CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("CHEM 161", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        requisite = build_requisite("or")
        requisite.add_tag(build_tag("CHEM", "161"))
        requisite.add_tag(build_tag("CHEM", "101"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_two_nest_courses_or_operation(self):
        data = "(PHYS 113 [Min Grade: D] or PHYS 101 [Min Grade: D]) or (CS 171 [Min Grade: D] or CS 143 [Min Grade: D] or ENGR 131 [Min Grade: D])"
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
        requisite = build_requisite("or")
        requisite.add_tag(build_tag("PHYS", "113"))
        requisite.add_tag(build_tag("PHYS", "101"))
        requisite.add_tag(build_tag("CS", "171"))
        requisite.add_tag(build_tag("CS", "143"))
        requisite.add_tag(build_tag("ENGR", "131"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_two_nest_courses_and_operation(self):
        data = "(PHYS 113 [Min Grade: D] and PHYS 101 [Min Grade: D]) and (CS 171 [Min Grade: D] and CS 143 [Min Grade: D] and ENGR 131 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 113", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CS 171", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("CS 143", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("ENGR 131", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
        ]
        requisite = build_requisite("and")
        requisite.add_tag(build_tag("PHYS", "113"))
        requisite.add_tag(build_tag("PHYS", "101"))
        requisite.add_tag(build_tag("CS", "171"))
        requisite.add_tag(build_tag("CS", "143"))
        requisite.add_tag(build_tag("ENGR", "131"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_two_nest_courses_or_and_operation(self):
        data = "(PHYS 113 [Min Grade: D] and PHYS 101 [Min Grade: D]) or (CS 171 [Min Grade: D] and CS 143 [Min Grade: D] and ENGR 131 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 113", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CS 171", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("CS 143", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("ENGR 131", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
        ]
        requisite = build_requisite("or")
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("PHYS", "113"))
        subrequisite.add_tag(build_tag("PHYS", "101"))
        requisite.add_tag(subrequisite)
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("CS", "171"))
        subrequisite.add_tag(build_tag("CS", "143"))
        subrequisite.add_tag(build_tag("ENGR", "131"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_two_nest_courses_and_or_operation(self):
        data = "(PHYS 113 [Min Grade: D] or PHYS 101 [Min Grade: D]) and (CS 171 [Min Grade: D] or CS 143 [Min Grade: D] or ENGR 131 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 113", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("PHYS 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CS 171", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("CS 143", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("ENGR 131", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
        ]
        requisite = build_requisite("and")
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("PHYS", "113"))
        subrequisite.add_tag(build_tag("PHYS", "101"))
        requisite.add_tag(subrequisite)
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("CS", "171"))
        subrequisite.add_tag(build_tag("CS", "143"))
        subrequisite.add_tag(build_tag("ENGR", "131"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_one_nest_course_start_asymmetrical_or_and_operation(self):
        data = "CHEM 246 [Min Grade: D] or (CHEM 241 [Min Grade: D] and CHEM 244 [Min Grade: D])"
        tokens = [
            build_token("CHEM 246", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 241", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 244", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        requisite = build_requisite("or")
        requisite.add_tag(build_tag("CHEM", "246"))
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("CHEM", "241"))
        subrequisite.add_tag(build_tag("CHEM", "244"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_one_nest_course_end_asymmetrical_or_and_operation(self):
        data = "(CHEM 241 [Min Grade: D] and CHEM 244 [Min Grade: D]) or CHEM 246 [Min Grade: D]"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 241", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 244", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("CHEM 246", TokenType.Course),
        ]
        requisite = build_requisite("or")
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("CHEM", "241"))
        subrequisite.add_tag(build_tag("CHEM", "244"))
        requisite.add_tag(subrequisite)
        requisite.add_tag(build_tag("CHEM", "246"))
        self.assertEqual(requisite, parse(tokens))

    def test_one_course_and_one_nest_course_start_asymmetrical_and_or_operation(self):
        data = "CHEM 101 [Min Grade: D] and (CHEM 111 [Min Grade: D] or CHEM 113 [Min Grade: D])"
        tokens = [
            build_token("CHEM 101", TokenType.Course),
            build_token("and", TokenType.AndOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 111", TokenType.Course),
            build_token("or", TokenType.AndOperation),
            build_token("CHEM 113", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        requisite = build_requisite("and")
        requisite.add_tag(build_tag("CHEM", "101"))
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("CHEM", "111"))
        subrequisite.add_tag(build_tag("CHEM", "113"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_one_nest_course_end_asymmetrical_and_or_operation(self):
        data = "(CHEM 111 [Min Grade: D] or CHEM 113 [Min Grade: D]) and CHEM 101 [Min Grade: D]"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("CHEM 111", TokenType.Course),
            build_token("or", TokenType.AndOperation),
            build_token("CHEM 113", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("and", TokenType.AndOperation),
            build_token("CHEM 101", TokenType.Course),
        ]
        requisite = build_requisite("and")
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("CHEM", "111"))
        subrequisite.add_tag(build_tag("CHEM", "113"))
        requisite.add_tag(subrequisite)
        requisite.add_tag(build_tag("CHEM", "101"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_two_nest_courses_middle_or_and_operation(self):
        data = "(PHYS 153 [Min Grade: D] and PHYS 101 [Min Grade: D]) or MATH 110 [Min Grade: C] and (MATH 121 [Min Grade: C] or MATH 101 [Min Grade: C])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 153", TokenType.Course),
            build_token("and", TokenType.OrOperation),
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
        requisite = build_requisite("or")
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("PHYS", "153"))
        subrequisite.add_tag(build_tag("PHYS", "101"))
        requisite.add_tag(subrequisite)
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("MATH", "110"))
        subsubrequisite = build_requisite("or")
        subsubrequisite.add_tag(build_tag("MATH", "121"))
        subsubrequisite.add_tag(build_tag("MATH", "101"))
        subrequisite.add_tag(subsubrequisite)
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_two_nest_courses_middle_and_or_operation(self):
        requisite = "(PHYS 153 [Min Grade: D] or PHYS 101 [Min Grade: D]) and MATH 110 [Min Grade: C] or (MATH 121 [Min Grade: C] and MATH 101 [Min Grade: C])"
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
            build_token("and", TokenType.OrOperation),
            build_token("MATH 101", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        requisite = build_requisite("or")
        subrequisite = build_requisite("and")
        subsubrequisite = build_requisite("or")
        subsubrequisite.add_tag(build_tag("PHYS", "153"))
        subsubrequisite.add_tag(build_tag("PHYS", "101"))
        subrequisite.add_tag(subsubrequisite)
        subrequisite.add_tag(build_tag("MATH", "110"))
        requisite.add_tag(subrequisite)
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("MATH", "121"))
        subrequisite.add_tag(build_tag("MATH", "101"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_two_nest_courses_middle_and_and_operation(self):
        data = "(PHYS 154 [Min Grade: D] or PHYS 102 [Min Grade: D]) and MATH 122 [Min Grade: D] and (MET 101 [Min Grade: D] or ENGR 220 [Min Grade: D])"
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
        requisite = build_requisite("and")
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("PHYS", "154"))
        subrequisite.add_tag(build_tag("PHYS", "102"))
        requisite.add_tag(subrequisite)
        requisite.add_tag(build_tag("MATH", "122"))
        subrequisite = build_requisite("or")
        subrequisite.add_tag(build_tag("MET", "101"))
        subrequisite.add_tag(build_tag("ENGR", "220"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_one_course_and_two_nest_courses_middle_or_or_operation(self):
        data = "(PHYS 154 [Min Grade: D] and PHYS 102 [Min Grade: D]) or MATH 122 [Min Grade: D] or (MET 101 [Min Grade: D] and ENGR 220 [Min Grade: D])"
        tokens = [
            build_token("(", TokenType.OpenParenthesis),
            build_token("PHYS 154", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("PHYS 102", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis),
            build_token("or", TokenType.OrOperation),
            build_token("MATH 122", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("(", TokenType.OpenParenthesis),
            build_token("MET 101", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("ENGR 220", TokenType.Course),
            build_token(")", TokenType.CloseParenthesis)
        ]
        requisite = build_requisite("or")
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("PHYS", "154"))
        subrequisite.add_tag(build_tag("PHYS", "102"))
        requisite.add_tag(subrequisite)
        requisite.add_tag(build_tag("MATH", "122"))
        subrequisite = build_requisite("and")
        subrequisite.add_tag(build_tag("MET", "101"))
        subrequisite.add_tag(build_tag("ENGR", "220"))
        requisite.add_tag(subrequisite)
        self.assertEqual(requisite, parse(tokens))
    
    def test_start_or_operation(self):
        data = "or BIO 122 [Min Grade: D] or BIO 141 [Min Grade: D] or BIO 131 [Min Grade: D]"
        tokens = [
            build_token("or", TokenType.OrOperation),
            build_token("BIO 122", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("BIO 141", TokenType.Course),
            build_token("or", TokenType.OrOperation),
            build_token("BIO 131", TokenType.Course)
        ]
        requisite = build_requisite("or")
        requisite.add_tag(build_tag("BIO", "122"))
        requisite.add_tag(build_tag("BIO", "141"))
        requisite.add_tag(build_tag("BIO", "131"))
        self.assertEqual(requisite, parse(tokens))
    
    def test_start_and_operation(self):
        data = "and BIO 122 [Min Grade: D] and BIO 141 [Min Grade: D] and BIO 131 [Min Grade: D]"
        tokens = [
            build_token("and", TokenType.OrOperation),
            build_token("BIO 122", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("BIO 141", TokenType.Course),
            build_token("and", TokenType.OrOperation),
            build_token("BIO 131", TokenType.Course)
        ]
        requisite = build_requisite("and")
        requisite.add_tag(build_tag("BIO", "122"))
        requisite.add_tag(build_tag("BIO", "141"))
        requisite.add_tag(build_tag("BIO", "131"))
        self.assertEqual(requisite, parse(tokens))

if __name__ == "__main__":
    unittest.main()