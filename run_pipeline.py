import sys
import io

import preprocess as prep
import question_generation as qg
import question_answering as qa

from pprint import PrettyPrinter
pp = PrettyPrinter()

'''
Main run loop for our QG/QA system.
Input: Text file
Output: List of questions generated from the text, list of answers generated from the text + questions
Usage: python run_pipeline.py INPUT_TXT
'''
if __name__ == "__main__":
    
    # Ensure 1 argument (besides the script itself)
    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py INPUT_TXT")
        sys.exit(1)

    # Read string from 1 text file. 
    # TODO: extend this to a directory of files
    INPUT_TXT = sys.argv[1]

    with open(INPUT_TXT, 'r') as file:
        text = file.read()

    print(text)

    # Instantiate our preprocessor and get the processed doc
    preprocesser = prep.Preprocessor(text)
    processed_doc = preprocesser.doc

    # Instantiate our question generator and make some questions
    question_generator = qg.QuestionGenerator()

    wh_questions = question_generator.generateWhQuestions(processed_doc)
    pp.pprint(wh_questions)

    # TODO: Expand question set with synonyms etc.
    # TODO: Filter question set for good questions
    # TODO: Given questions (or fake questions), generate some answers!

