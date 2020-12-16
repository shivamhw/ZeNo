
class Parser:
    def marks_parser(raw_data):
        output_string = 'Results: \n\n'
        for i in raw_data:
            output_string += str(i['name']) + " : \n" \
                            + i['c1_marks'] + ' | ' \
                            + i['c2_marks'] + ' | ' \
                            + i['c3_marks'] + '\n\n'
        return output_string
