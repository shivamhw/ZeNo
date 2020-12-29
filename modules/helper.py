
class Parser:
    def marks_parser(raw_data):
        output_string = 'Results: \n\n'
        for i in raw_data:
            output_string += str(i['name']) + " : \n" \
                            + i['c1_marks'] + ' | ' \
                            + i['c2_marks'] + ' | ' \
                            + i['c3_marks'] + ' = ' \
                            + i['total'] + '\n' \
                            +"GPA = "+ i['gpa'] +'\n\n'
        if output_string == 'Results: \n\n':
            output_string = "\nNo Results for this session.."
        return output_string

    def percentile(marks_analytics):
        total_students = marks_analytics[0] + marks_analytics[1] + marks_analytics[2]+1
        percentile = (marks_analytics[0]+marks_analytics[2]+1)/total_students*100
        return percentile

class Pages:
    faq = ("1. Why use Zeno?"
           "\n\nAns. it is fast than aviral website and provides information more efficiently than any whatsapp group,"
           "\nbut the main reason to use Zeno is because you can view code and tinker around with stuff. " 
           "You can see how a fun little project can scale or fail at production enviroment and try to fix the problems yourself"
           "\n\n2. What about privacy?"
           "\n\nAns. Zeno works with token so it just saves your session with aviral. at no point of time your password is stored in any DB."
           )
    about = ("Zeno started as a fun project but became a part of developers life."
             "\n\nIt is here to provide a single point of contact for IIITA students so they dont need to switch between different platform to get something done."
             "\n\nGitHub : bit.ly/zeno-iiita (PRIVATE FOR NOW.)"
             )
    pages = {'about': about, 'faq': faq}
    def get_note(note):
        return Pages.pages[note]