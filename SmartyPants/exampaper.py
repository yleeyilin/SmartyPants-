import streamlit as st
from toolkit import pdf_to_txt, split, prompt, generate_pdf, convert_to_pdf
from langchain import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser

warning = """
This app generates exam papers with questions and answers, powered by GPT-3. You can download the questions as a PDF file. 
However, please note that the accuracy of the generated questions may vary depending on the topic. 
It is recommended to verify the information by searching online or consulting an expert.

Please keep in mind that this app is for educational purposes only. 
It is designed to help students practice and test their knowledge, and it is not intended for creating exam papers in real-world scenarios.
"""

def generate_html(exam_data):
    html = "<html><body>"
    html += "<h1>MCQ Exam Paper</h1>"
    for index, question in enumerate(exam_data):
        html += f"<h2>Question {index+1}</h2>"
        html += f"<p>{question['question']}</p>"
        for option in question['options']:
            html += f"<label><input type='radio' name='question-{index+1}'> {option}</label><br>"
    html += "</body></html>"
    return html

def exampapers(llm):
    chain = load_qa_chain(llm, chain_type="stuff")
    output_parser = CommaSeparatedListOutputParser()
    uploaded_file = st.file_uploader("Upload Exam PDF file", type="pdf")
    if uploaded_file is not None:
        st.markdown(warning)
        txt_file = pdf_to_txt(uploaded_file)
        if txt_file is not None:
            tpz = chain.run(input_documents=split("Key Topics", txt_file), question="What are the main topics here? Separate each topic with a ,")
            topics = tpz.split(",")
            numQuestions = st.number_input(
                "Number of questions",
                min_value=5,
                max_value=30,
                value=10,
                help="Number of questions that will be generated"
            )
            if st.button("Generate"):
                st.warning("Generating questions. This may take a while...")
                try:
                    promptt = prompt(topics, numQuestions)
                    template = PromptTemplate(template=promptt, input_variables=[], output_parser=output_parser)
                    llm_chain = LLMChain(prompt=template, llm=llm)
                    res = llm_chain.predict_and_parse()
                    print(res)
                    pdf_bytes = convert_to_pdf(res)
                    if pdf_bytes:
                        st.success("Questions generated successfully!")
                        st.download_button("Download Exam Paper", data=pdf_bytes, file_name="exam_paper.pdf", mime="application/pdf")
                    else:
                        st.error("Error occurred during PDF generation. Please try again.")
                except Exception as e:
                    st.error("Error occurred during question generation. Please try again.")