# Document Intelligence System (Local AI Reader)

This is a private, secure web app that lets you upload a PDF document and ask questions about it. Instead of sending your file to an outside company over the internet, a small, highly capable AI model reads and answers everything directly on your own computer.

---

### How It Works

Think of this app as an assistant working in a secure room:
1. **The Library:** You upload a PDF. The app chops it up page by page.
2. **The Search:** When you ask a question, the app quickly scans the pages for matching keywords to find the exact paragraph containing the answer.
3. **The Answer:** The app hands just that relevant paragraph to your local AI model, which reads it and writes a smart, clean answer for you.

---

### Key Features

* ** 100% Private & Safe:** Your documents never leave your computer. Because the AI runs entirely offline, no external servers see your private data. 
* ** Quick Action Buttons:** Instantly summarize a document into 3 bullet points or extract main skills and topics with a single click—no typing required.
* ** Premium Clean Design:** Designed with a distraction-free dark theme that looks clean and professional.

---

### Built With

* **Streamlit:** Creates the user interface and input boxes.
* **PyPDF2:** Reads and extracts the text from your uploaded PDF.
* **Ollama:** The background program that runs the AI model directly on your computer's processor.
* **Llama 3.2:** A powerful open-source AI model created by Meta (Facebook) that runs locally.

---

### How to Run It on Your Computer

#### 1. Start the AI Engine
1. Download and install [Ollama](https://ollama.com/).
2. Open your computer's command prompt terminal and run the model:
   ```bash
   ollama run llama3.2
