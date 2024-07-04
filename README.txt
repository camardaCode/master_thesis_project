=====================================================
    Notes for the reproducibility of the project
=====================================================

Given the need for high-performance hardware with a large RAM memory to run LLaMA 3, the project uses a Kaggle notebook which is saved to disk each time and then updated on Kaggle itself. Furthermore, a private dataset is also used in which to load the files that you want to give as input to the LLM.

However, the notebook is also private, so before you can use LLaMA you need to:
1. create your own kaggle account;
2. request permission to access the Meta model (LLaMA 3-8B Instruct). Permission is granted individually to the user who requests it;
3. create a new notebook where you can copy the code of the already tested and working notebook;
4. create a dataset with the same name as the one already mentioned in the notebook.

Note also that to use GPT during the execution of the project, you need to pay every request made using OpenAI-API. For this reason, before you can use GPT you need to:
1. create your own OpenAI account;
2. provide your debit card information in order to access the API.