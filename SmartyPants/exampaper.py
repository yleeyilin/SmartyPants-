import streamlit as st
import pdfplumber
import openai

# Function to identify the question format
def identify_question_format(question_text):
    # Add your logic to identify the question format
    # You can use regular expressions, keyword matching, or any other method

    # For demonstration purposes, let's assume all questions are multiple-choice
    return 'multiple_choice'

def generate_similar_question(question):
    # Use OpenAI language model to generate a similar question based on the input question
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=100,
        n=1,  # Generate a single similar question
        stop=None,
        temperature=0.7
    )

    similar_question = response['choices'][0]['text']
    return similar_question

def generate_exam_paper(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        # Extract text from each page
        exam_text = ""
        for page in pdf.pages:
            exam_text += page.extract_text()

        # Split the exam text into individual questions (assuming each question ends with a question mark)
        questions = exam_text.split('?')

        generated_questions = []
        for question in questions:
            # Identify the question format
            question_format = identify_question_format(question)

            # Generate a similar question
            similar_question = generate_similar_question(question)

            # Append the similar question to the generated questions list
            generated_questions.append(similar_question)

    return generated_questions

def main():
    st.title("Exam Paper Generator")

    # File uploader
    uploaded_file = st.file_uploader("Upload Exam PDF file", type="pdf")

    if uploaded_file is not None:
        # Generate the exam paper
        generated_questions = generate_exam_paper(uploaded_file)

        # Display the generated exam paper
        st.write("Generated Exam Paper:")
        for question in generated_questions:
            st.write(question)

# Run the main function
if __name__ == "__main__":
    main()


# def identify_question_format(question_text):
#     format_regexes = {
#         'multiple_choice': r'\b[A-D]\)',
#         'true_false': r'\b(True|False)\b',
#         'short_answer': r'(?:Answer: )(.+)',
#         # other question formats
#     }

#     # iterate over the regex patterns and check for matches
#     for question_format, pattern in format_regexes.items():
#         if re.search(pattern, question_text):
#             return question_format
        
#     # if no matches are found
#     return None

# def exampapers():
#     uploaded_file = st.file_uploader('Upload Exam PDF file', type='pdf')

#     if uploaded_file is not None: 
#         # extract content from uploaded exam paper
#         with pdfplumber.open(uploaded_file) as pdf:
#             # extract text from each page
#             exam_text = ""
#             for page in pdf.pages:
#                 exam_text += page.extract_text()

#                 # split the exam text into individual questions (assuming each ends with '?')
#                 questions = re.split(r'\?\s*', exam_text)

#                 # iterate over each question and identify question format
#                 for question in questions:
#                     question_format = identify_question_format(question)
#                     if question_format is not None:
#                         # do something with the identified question format

#             # parse and analyse exam content

#         #generate new questions using openAI
#         generated_questions = openai.Completion.create(
#             engine="text-davinci-003",
#             prompt="Prompt text here",
#             max_tokens = 100,
#             n=10,
#             stop=None,
#             temperature=0.7
#         )

#         # extract the generated questions from the API response
#         generated_questions = [question['choices'][0]['text'] for question in generated_questions['choices']]

#         # format and present the generated exam paper
#         st.write("Generated Exam Paper:")
#         for question in generated_questions:
#             st.write(question)

#         # call the exampapers() function
#         exampapers()
