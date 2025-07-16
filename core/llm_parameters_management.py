from langchain_openai import ChatOpenAI

llm, llm_choose = None, None

LLM_INFO_LIST = [
    ['qwen-plus', 'sk-7cf8cbdcf35a408ba7bac7d9cd3b0c4c'],
    ['deepseek-r1', 'sk-7cf8cbdcf35a408ba7bac7d9cd3b0c4c'],
]
llm_li = []


class LLM:
    def __init__(self, api_key, temperature=0, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        self.api_key = api_key
        self.temperature = temperature
        self.base_url = base_url
    
    def generator_llm_obj(self):
        raise NotImplementedError
    
    def switch(self):
        raise NotImplementedError


class ALI(LLM):
    def __init__(self, model_name, api_key, temperature=0, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"):
        super().__init__(api_key, temperature, base_url)
        self.model = model_name
        self.generator_llm_obj()

    def generator_llm_obj(self):
        self.llm = ChatOpenAI(
                    api_key=self.api_key,
                    model =self.model,
                    base_url=self.base_url,
                    temperature=self.temperature,
                    )
    
    def switch(self):
        global llm, llm_choose
        llm_choose = self
        llm = self.llm

for item in LLM_INFO_LIST:
    obj = ALI(*item)
    llm_li.append(obj)

llm_li[0].switch()
