                         
<br/>
<div align="center">

<h3 align="center">Better Cover Letter Generator</h3>
<p align="center">
Next-Gen Cover Letter Generator with LLM & Snowflake.

<br/>
<br/>
<a href="https://better-coverletter-generator.streamlit.app/">View Demo</a>  
<a href="https://github.com/lingyundai/snowflake-hackathon/issues/new">Report Bug</a>
<a href="https://github.com/lingyundai/snowflake-hackathon/issues/new">Request Feature</a>
</p>
</div>

 ## About The Application

![Final Screen](https://raw.githubusercontent.com/lingyundai/snowflake-hackathon/main/Images/Landing_page.png)

Many cover letter generators take minimal information and generate a terrible cover letter that anyone can detect is generated with AI
- Robotic words and inaccurate information provide no substantial information that the hiring manager wants to see 
- Repetitive content, too generalized.
Result In 'Unfortunately...' e-mails, bad impression, frustration, time wasted for both parties.

This application will fix that!! Hopefully, in these ways
- We use comprehensive information to generate a detailed, useful cover letter for the job type you are applying to.
- We keep a history of the files you uploaded, over time, the cover letter just gets more and more personalized for you and your desired job type.
- Chat GPT? NO! We use the Snowflake LLM technology 'mistral-large' that generates high-quality models.

In the end, we are in this together. 

Happy generating!

 ### Built With

- [Snowflake Connector for Python](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector)
- [Streamlit](https://docs.streamlit.io/)
- [Snowflake](https://docs.snowflake.com/)
- [PyPdf](https://pypdf.readthedocs.io/en/stable/)
- [Python Docx](https://python-docx.readthedocs.io/en/latest/)
 ## Getting Started

- Run this command in your local where the project folder is located-
  ```sh
  pip install -r requirements.txt
  ```
 ### Installation

1. Create an account at [Snowflake Sign Up](https://signup.snowflake.com/?referrer=snowsight)
2. Clone the repo
   ```sh
   git clone https://github.com/lingyundai/snowflake-hackathon.git
   ```
3. Run this command-
   ```sh
    pip install -r requirements.txt
   ```
4. Run the application
   ```sh
    streamlit run app.py
   ```
5. The application will ask you to enter your snowflake credentials. 
 - For the field "Snowflake Account", copy the link that you get after signing in to Snowflake (step 1). In that, enter the code in place of "account".
```sh
For example - https://[account].snowflakecomputing.com/
   ```
6. In the user name and password prompted by the application, enter your Snowflake credentials.
 ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
 ## License

Distributed under the MIT License. See [MIT License](https://opensource.org/licenses/MIT) for more information.
