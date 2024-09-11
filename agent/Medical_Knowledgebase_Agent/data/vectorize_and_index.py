import fitz
import docx
import os
import json
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
import numpy as np
import pandas as pd
import tqdm
# 加载配置文件
with open('/root/autodl-tmp/MedicaAgent/agent/chatbotagent/config.json', encoding='utf-8') as config_file:
    config = json.load(config_file)

def pdf_to_text(pdf_path):
    doc = fitz.open(pdf_path)       # 打开PDF文件
    text = ""
    for page in doc:
        text += page.get_text()     # 从每一页提取文本并累加到text字符串中
    return text

def docx_to_text(docx_path):
    doc = docx.Document(docx_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"    # 提取每一段的文本并累加到text字符串中
    return text

def excel_to_text(excel_path):
    df = pd.read_excel(excel_path)  # 读取Excel文件
    text = df.to_string(index=False)  # 将数据框转换为字符串表示
    return text

def txt_to_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def json_to_text(json_path):
    text = ""
    with open(json_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())  # 逐行加载JSON数据
            if 'text' in data:
                text += data['text'] + "\n"  # 提取每行的"text"字段
    return text

def file_to_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()  # 获取文件扩展名并转为小写
    if ext == ".pdf":
        return pdf_to_text(file_path)
    elif ext == ".docx":
        return docx_to_text(file_path)
    elif ext in [".xls", ".xlsx"]:
        return excel_to_text(file_path)
    elif ext == ".txt":
        return txt_to_text(file_path)
    elif ext == ".json":
        return json_to_text(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


# 生成知识库向量及索引
def create_vector_index(texts, embedding_model_path, index_path, vector_data_path, text_mapping_path):
    tokenizer = AutoTokenizer.from_pretrained(embedding_model_path)  # 加载embedding模型分词器
    model = AutoModel.from_pretrained(embedding_model_path,trust_remote_code=True) 
    # 加载embedding模型

    def encode(texts):
        inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            outputs = model(**inputs)

        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings

    chunks = [texts[i:i+config['chunk_size']] for i in tqdm.tqdm(range(0, len(texts), config['chunk_size']))]    # 生成chunks
    vectors = np.vstack([encode(chunk).cpu().numpy() for chunk in tqdm.tqdm(chunks)])  # 使用模型进行embedding

    # 保存文本块与索引的映射
    text_mapping = {i: chunks[i] for i in tqdm.tqdm(range(len(chunks)))}
    with open(text_mapping_path, 'w', encoding='utf-8') as f:
        json.dump(text_mapping, f, ensure_ascii=False, indent=4)

    dimension = vectors.shape[1]            # 获取向量的维度
    index = faiss.IndexFlatL2(dimension)    # 创建一个FAISS索引，用于L2距离的快速相似性搜索
    index.add(vectors)                      # 将向量添加到索引中
    faiss.write_index(index, index_path)    # 将索引写入指定路径的文件中
    np.save(vector_data_path, vectors)      # 保存向量到指定路径的文件中


if __name__ == "__main__":
    text = file_to_text(config['rag_data_path'])  # 从配置中读取PDF路径，并提取PDF文本

    # 创建向量索引并保存 其中，vector_db_path如果报错找不到文件，则将绝对路径更换为相对路径
    create_vector_index(text, config['embedding_model_path'], config['vector_dbindex_path'], config['vector_vectors_path'], config['text_mapping_path'])
