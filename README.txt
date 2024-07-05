=====================================================
                      Abstract
=====================================================

Digital devices are increasingly present in our daily life. When investigations on crimes take place, it is often necessary to look for evidence within these devices. Consequently, the collection and the analysis of evidence, as well as the entire investigation process is digital nowadays. This brought to the development of artificial intelligence and automation methods, and of dedicated software whose purpose is to support every phase of the investigative process. In this context, it has been proposed the STeForTAI paradigm: a Socio-Technical Framework for Trustworthy Artificial Intelligence in Digital Forensics, whose aim is to integrate automated reasoning methods into digital forensics. 
This formal proposal of the framework has not been followed by practical implementations yet, thus leaving open the question whether technical limitations hinder the possibility of a concrete realization of the framework. In this thesis work, we provide a first practical approach to the implementation of STeForTAI. In particular, we propose a combination of one of the most used declarative languages in the state-of-art, Answer Set Programming, with the increasingly popular Large Language Models, and with a freely available commonsense knowledge base, ConceptNet.


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
