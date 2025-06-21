from __future__ import annotations
from google import genai
import os
import logging
import json
from datetime import datetime

# Configure logging
log_directory = os.getenv("LOG_DIR", "logs")
os.makedirs(log_directory, exist_ok=True)
log_file = os.path.join(
    log_directory, f"llm_calls_{datetime.now().strftime('%Y%m%d')}.log"
)

# Set up logger
logger = logging.getLogger("llm_logger")
logger.setLevel(logging.INFO)
logger.propagate = False  # Prevent propagation to root logger
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Simple cache configuration
cache_file = "llm_cache.json"


# By default, we Google Gemini 2.5 pro, as it shows great performance for code understanding
# def call_llm(prompt: str, use_cache: bool = True) -> str:
#     # Log the prompt
#     logger.info(f"PROMPT: {prompt}")

#     # Check cache if enabled
#     if use_cache:
#         # Load cache from disk
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except:
#                 logger.warning(f"Failed to load cache, starting with empty cache")

#         # Return from cache if exists
#         if prompt in cache:
#             logger.info(f"RESPONSE: {cache[prompt]}")
#             return cache[prompt]

#     # # Call the LLM if not in cache or cache disabled
#     # client = genai.Client(
#     #     vertexai=True,
#     #     # TODO: change to your own project id and location
#     #     project=os.getenv("GEMINI_PROJECT_ID", "your-project-id"),
#     #     location=os.getenv("GEMINI_LOCATION", "us-central1")
#     # )

#     # You can comment the previous line and use the AI Studio key instead:
#     client = genai.Client(
#         api_key=os.getenv("GEMINI_API_KEY", "API_KEY"),
#     )
#     model = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
#     # model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-04-17")

#     response = client.models.generate_content(model=model, contents=[prompt])
#     response_text = response.text

#     # Log the response
#     logger.info(f"RESPONSE: {response_text}")

#     # Update cache if enabled
#     if use_cache:
#         # Load cache again to avoid overwrites
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except:
#                 pass

#         # Add to cache and save
#         cache[prompt] = response_text
#         try:
#             with open(cache_file, "w", encoding="utf-8") as f:
#                 json.dump(cache, f)
#         except Exception as e:
#             logger.error(f"Failed to save cache: {e}")

#     return response_text


# # Use Azure OpenAI
# def call_llm(prompt, use_cache: bool = True):
#     from openai import AzureOpenAI

#     endpoint = "https://<azure openai name>.openai.azure.com/"
#     deployment = "<deployment name>"

#     subscription_key = "<azure openai key>"
#     api_version = "<api version>"

#     client = AzureOpenAI(
#         api_version=api_version,
#         azure_endpoint=endpoint,
#         api_key=subscription_key,
#     )

#     r = client.chat.completions.create(
#         model=deployment,
#         messages=[{"role": "user", "content": prompt}],
#         response_format={
#             "type": "text"
#         },
#         max_completion_tokens=40000,
#         reasoning_effort="medium",
#         store=False
#     )
#     return r.choices[0].message.content

# # Use Anthropic Claude 3.7 Sonnet Extended Thinking
# def call_llm(prompt, use_cache: bool = True):
#     from anthropic import Anthropic
#     client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", "your-api-key"))
#     response = client.messages.create(
#         model="claude-3-7-sonnet-20250219",
#         max_tokens=21000,
#         thinking={
#             "type": "enabled",
#             "budget_tokens": 20000
#         },
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.content[1].text


# Use OpenAI o1
# def call_llm(prompt, use_cache: bool = True):
#     from openai import OpenAI

#     client = OpenAI(
#         api_key=os.environ.get(
#             "OPENAI_API_KEY",
#             "API_KEY",
#         )
#     )
#     r = client.chat.completions.create(
#         model="o1",
#         messages=[{"role": "user", "content": prompt}],
#         response_format={"type": "text"},
#         reasoning_effort="medium",
#         store=False,
#     )
#     return r.choices[0].message.content


# Use OpenRouter API
# def call_llm(prompt: str, use_cache: bool = True) -> str:
#     import requests
#     # Log the prompt
#     logger.info(f"PROMPT: {prompt}")

#     # Check cache if enabled
#     if use_cache:
#         # Load cache from disk
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except:
#                 logger.warning(f"Failed to load cache, starting with empty cache")

#         # Return from cache if exists
#         if prompt in cache:
#             logger.info(f"RESPONSE: {cache[prompt]}")
#             return cache[prompt]

#     # OpenRouter API configuration
#     api_key = os.getenv("OPENROUTER_API_KEY", "")
#     model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-exp:free")

#     headers = {
#         "Authorization": f"Bearer {api_key}",
#     }

#     data = {
#         "model": model,
#         "messages": [{"role": "user", "content": prompt}]
#     }

#     response = requests.post(
#         "https://openrouter.ai/api/v1/chat/completions",
#         headers=headers,
#         json=data
#     )

#     if response.status_code != 200:
#         error_msg = f"OpenRouter API call failed with status {response.status_code}: {response.text}"
#         logger.error(error_msg)
#         raise Exception(error_msg)
#     try:
#         response_text = response.json()["choices"][0]["message"]["content"]
#     except Exception as e:
#         error_msg = f"Failed to parse OpenRouter response: {e}; Response: {response.text}"
#         logger.error(error_msg)
#         raise Exception(error_msg)


#     # Log the response
#     logger.info(f"RESPONSE: {response_text}")

#     # Update cache if enabled
#     if use_cache:
#         # Load cache again to avoid overwrites
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except:
#                 pass

#         # Add to cache and save
#         cache[prompt] = response_text
#         try:
#             with open(cache_file, "w", encoding="utf-8") as f:
#                 json.dump(cache, f)
#         except Exception as e:
#             logger.error(f"Failed to save cache: {e}")

#     return response_text


# def call_llm(
#     prompt: str, use_cache: bool = True
# ) -> str:  # 注意这里添加了 use_cache 参数
#     # Log the prompt (truncated)
#     logger.info(f"PROMPT: {prompt[:500]}... [truncated]")

#     # Check cache if enabled
#     if use_cache:
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except Exception as e:
#                 logger.warning(f"Cache load error: {e}")

#         if prompt in cache:
#             cached_response = cache[prompt]
#             logger.info(f"RESPONSE (cached): {cached_response[:200]}...")
#             return cached_response

#     # 新增：长度检查与分块处理
#     import time

#     MAX_PROMPT_TOKENS = 60000  # 预留安全边界
#     CHUNK_SIZE = 15000  # 分块大小

#     if len(prompt) > MAX_PROMPT_TOKENS * 4:  # 保守估算: 1 token ≈ 4字符
#         logger.warning("Prompt too long, splitting into chunks...")

#         # 分块处理逻辑
#         chunks = [prompt[i : i + CHUNK_SIZE] for i in range(0, len(prompt), CHUNK_SIZE)]

#         responses = []
#         for chunk in chunks:
#             # 递归处理每个分块
#             response = call_llm(chunk, use_cache=False)  # 禁用分块缓存
#             responses.append(response)
#             time.sleep(1)  # 避免速率限制

#         return "\n\n".join(responses)

#     # 使用官方推荐的OpenAI库调用方式
#     from openai import OpenAI

#     try:
#         # 从环境变量获取API密钥
#         api_key = os.getenv("DEEPSEEK_API_KEY", "sk-b6675fce3b704310bbdbe9946da77530")

#         # 创建客户端
#         client = OpenAI(
#             api_key=api_key,
#             base_url="https://api.deepseek.com",  # 确保包含/v1路径
#         )

#         # 发送请求
#         response = client.chat.completions.create(
#             model="deepseek-reasoner",  # 或使用"deepseek-chat"
#             messages=[{"role": "user", "content": prompt}],
#             # temperature=0.3,
#             max_tokens=65536,
#             timeout=60,
#         )

#         # 提取响应内容
#         response_text = response.choices[0].message.content.strip()

#     except Exception as e:
#         # 详细的错误处理
#         error_msg = f"DeepSeek API error: {str(e)}"
#         logger.error(error_msg)

#         # 检查特定错误类型
#         if "context_length_exceeded" in str(e):
#             logger.error("提示过长，请减少输入内容")
#         elif "invalid_api_key" in str(e):
#             logger.error("API密钥无效，请检查环境变量")
#         elif "rate_limit" in str(e):
#             logger.error("达到API速率限制，请稍后重试")

#         raise RuntimeError(error_msg)

#     # Log the response (truncated)
#     logger.info(f"RESPONSE: {response_text[:200]}...")

#     # Update cache if enabled
#     if use_cache and response_text.strip():
#         try:
#             # 重新加载缓存
#             cache = {}
#             if os.path.exists(cache_file):
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)

#             # 添加响应到缓存
#             cache[prompt] = response_text
#             with open(cache_file, "w", encoding="utf-8") as f:
#                 json.dump(cache, f, indent=2, ensure_ascii=False)
#         except Exception as e:
#             logger.error(f"Failed to save cache: {e}")

#     return response_text


# def call_llm(prompt: str, use_cache: bool = True) -> str:
#     # Log the prompt (截断日志以防过大)
#     logger.info(f"PROMPT: {prompt[:500]}... [truncated]")

#     # Check cache if enabled
#     if use_cache:
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except Exception as e:
#                 logger.warning(f"Cache load error: {e}")

#         # Return from cache if exists
#         if prompt in cache:
#             logger.info(f"RESPONSE (cached): {cache[prompt][:200]}...")
#             return cache[prompt]

#     # Call DeepSeek API with enhanced error handling
#     import requests

#     api_key = os.getenv("DEEPSEEK_API_KEY", "sk-b6675fce3b704310bbdbe9946da77530")
#     model = os.getenv("DEEPSEEK_MODEL", "deepseek-coder")

#     headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

#     # 优化请求参数
#     payload = {
#         "model": model,
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.3,  # 降低温度以提高稳定性
#         "max_tokens": 131072,  # 确保不超过模型限制
#         "top_p": 0.9,
#         "stream": False,
#     }

#     try:
#         # 添加详细调试日志
#         logger.debug(f"Sending request to DeepSeek API with model: {model}")

#         response = requests.post(
#             "https://api.deepseek.com/v1/chat/completions",
#             headers=headers,
#             json=payload,
#             timeout=180,  # 增加超时时间
#         )

#         # 添加响应状态日志
#         logger.debug(f"API response status: {response.status_code}")

#         # 检查HTTP错误
#         if response.status_code != 200:
#             error_detail = (
#                 response.text[:500] + "..."
#                 if len(response.text) > 500
#                 else response.text
#             )
#             logger.error(f"API error {response.status_code}: {error_detail}")
#             raise RuntimeError(
#                 f"DeepSeek API error {response.status_code}: {response.reason}"
#             )

#         response_data = response.json()

#         # 验证响应结构
#         if "choices" not in response_data or len(response_data["choices"]) == 0:
#             logger.error(f"Invalid API response: {response_data}")
#             raise RuntimeError("Invalid API response structure")

#         response_text = response_data["choices"][0]["message"]["content"].strip()

#     except requests.exceptions.RequestException as e:
#         logger.error(f"Network error: {str(e)}")
#         raise RuntimeError(f"API connection failed: {str(e)}")
#     except (KeyError, IndexError) as e:
#         logger.error(f"Response parsing error: {str(e)}")
#         raise RuntimeError(f"Failed to parse API response: {str(e)}")
#     except json.JSONDecodeError as e:
#         logger.error(f"JSON decode error: {str(e)}")
#         raise RuntimeError(f"Invalid JSON response from API")
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         raise RuntimeError(f"API call failed: {str(e)}")

#     # Log the response (截断日志)
#     logger.info(f"RESPONSE: {response_text[:200]}...")

#     # Update cache if enabled
#     if use_cache:
#         try:
#             # 重新加载缓存以防并发修改
#             cache = {}
#             if os.path.exists(cache_file):
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)

#             # 仅当响应有效时缓存
#             if response_text.strip():
#                 cache[prompt] = response_text
#                 with open(cache_file, "w", encoding="utf-8") as f:
#                     json.dump(cache, f, indent=2, ensure_ascii=False)
#         except Exception as e:
#             logger.error(f"Cache update failed: {e}")

#     return response_text


# def call_llm(prompt: str, use_cache: bool = True) -> str:
#     # Log the prompt (truncated)
#     logger.info(f"PROMPT: {prompt[:500]}... [truncated]")

#     # Check cache if enabled
#     if use_cache:
#         cache = {}
#         if os.path.exists(cache_file):
#             try:
#                 with open(cache_file, "r", encoding="utf-8") as f:
#                     cache = json.load(f)
#             except Exception as e:
#                 logger.warning(f"Cache load error: {e}")

#         if prompt in cache:
#             logger.info(f"RESPONSE (cached): {cache[prompt][:200]}...")
#             return cache[prompt]

#     # Call local DeepSeek-R1-Distill-Qwen-7B API
#     import requests

#     api_url = "http://192.168.1.90:12345/v1/chat/completions"

#     headers = {"Content-Type": "application/json"}

#     # 优化请求参数以解决 prediction-error
#     payload = {
#         "model": "deepseek-r1-distill-qwen-7b",
#         "messages": [
#             {"role": "system", "content": "You are a helpful AI assistant."},
#             {"role": "user", "content": prompt},
#         ],
#         "temperature": 0.5,  # 降低温度提高稳定性
#         "max_tokens": -1,  # 减少输出长度避免错误
#         # "top_p": 0.9,
#         # "frequency_penalty": 0.2,  # 减少重复
#         # "presence_penalty": 0.2,  # 鼓励新内容
#         # "stop": ["<|endoftext|>", "</s>", "\n\n\n"],  # 添加停止词
#         "stream": False,
#     }

#     try:
#         logger.debug(f"Sending request to local API: {api_url}")

#         # 增加超时时间并添加重试机制
#         for attempt in range(3):
#             try:
#                 response = requests.post(
#                     api_url,
#                     headers=headers,
#                     json=payload,
#                     timeout=180,  # 更长的超时时间
#                 )

#                 # 检查响应状态
#                 if response.status_code == 200:
#                     response_data = response.json()
#                     break
#                 elif (
#                     response.status_code == 500 and "prediction-error" in response.text
#                 ):
#                     logger.warning(
#                         f"Prediction error on attempt {attempt+1}, retrying..."
#                     )
#                     continue
#                 else:
#                     response.raise_for_status()
#             except (
#                 requests.exceptions.Timeout,
#                 requests.exceptions.ConnectionError,
#             ) as e:
#                 if attempt < 2:
#                     logger.warning(
#                         f"Connection error on attempt {attempt+1}, retrying..."
#                     )
#                     continue
#                 else:
#                     raise

#         # 验证响应结构
#         if "choices" not in response_data or len(response_data["choices"]) == 0:
#             error_msg = (
#                 f"Invalid API response: {json.dumps(response_data, indent=2)[:500]}"
#             )
#             logger.error(error_msg)
#             raise RuntimeError("Invalid API response structure")

#         # 提取响应内容
#         response_text = response_data["choices"][0]["message"]["content"].strip()

#     except requests.exceptions.RequestException as e:
#         logger.error(f"API connection error: {str(e)}")
#         raise RuntimeError(f"Local API connection failed: {str(e)}")
#     except (KeyError, IndexError) as e:
#         logger.error(f"API response parsing error: {str(e)}")
#         raise RuntimeError(f"Failed to parse API response: {str(e)}")
#     except Exception as e:
#         logger.error(f"Unexpected error: {str(e)}")
#         raise RuntimeError(f"API call failed: {str(e)}")

#     # Log the response (truncated)
#     logger.info(f"RESPONSE: {response_text[:200]}...")

#     # Update cache if enabled
#     if use_cache:
#         try:
#             # 重新加载缓存
#             cache = {}
#             if os.path.exists(cache_file):
#                 try:
#                     with open(cache_file, "r", encoding="utf-8") as f:
#                         cache = json.load(f)
#                 except:
#                     pass

#             # 添加响应到缓存
#             cache[prompt] = response_text
#             with open(cache_file, "w", encoding="utf-8") as f:
#                 json.dump(cache, f, indent=2, ensure_ascii=False)
#         except Exception as e:
#             logger.error(f"Failed to save cache: {e}")

#     return response_text


import json
import logging
import os
import re
from typing import List

from openai import OpenAI

try:
    import tiktoken  # 可选：更精确地估算 token
except ImportError:  # noqa: WPS440
    tiktoken = None

# 配置日志
logger = logging.getLogger(__name__)
cache_file = "llm_cache.json"


DEFAULT_MAX_CHARS = 16_000  # 默认最大块大小
DEFAULT_MODEL = "deepseek-r1-distill-qwen-14b"
BASE_URL = "http://localhost:12345/v1"  # "https://api.deepseek.com"

CACHE_FILE = "llm_cache.json"
MAX_RECURSION_DEPTH = 10  # 防御式：最多切 10 层

# logger 基础配置
logger = logging.getLogger(__name__)
if not logger.handlers:  # 防止在交互式环境里重复添加 handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(levelname)s %(asctime)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # 或 DEBUG
logger.propagate = False


# ─────────────────────────── 工 具 / 辅 助 ────────────────────────────
def _force_slice(text: str, max_size: int) -> List[str]:
    """最后兜底：按字符硬切，保证每块 ≤ max_size。"""
    return [text[i : i + max_size] for i in range(0, len(text), max_size)]  # noqa: E203


def split_prompt(prompt: str, max_size: int = DEFAULT_MAX_CHARS) -> List[str]:
    """
    智能分割提示文本为多个块：

    1. 尝试按  `File:` （常见于 diff / code-review）切分
    2. 尝试按 `class / def` 切分
    3. 按行切分
    4. 任何仍超长的部分 → _force_slice

    永远保证返回的每个 chunk 都 <= max_size。
    """
    # ① File 级
    file_sections = re.split(r"(?=File:\s+)", prompt)
    if len(file_sections) > 1:
        return _smart_concat(file_sections, max_size)

    # ② class/def 级
    class_sections = re.split(r"(?=class\s+\w+\s*:|def\s+\w+\()", prompt)
    if len(class_sections) > 1:
        return _smart_concat(class_sections, max_size)

    # ③ 行级 + 兜底
    return _smart_concat(prompt.splitlines(keepends=True), max_size)


def _smart_concat(sections: List[str], max_size: int) -> List[str]:
    """
    把若干 section 拼成块：如果 section 太大就 _force_slice，再保证
    current_chunk 不超过 max_size。
    """
    chunks, current = [], ""
    for sec in sections:
        if not sec:
            continue
        # 先兜底切超巨 section
        if len(sec) > max_size:
            # 之前累积的 current 先收尾
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_force_slice(sec, max_size))
            continue

        if len(current) + len(sec) > max_size:
            if current:
                chunks.append(current)
            current = sec
        else:
            current += sec
    if current:
        chunks.append(current)
    return chunks


def estimate_token_count(text: str) -> int:
    """
    估算文本 token 数量。
    • 若安装了 tiktoken，则按 gpt-2 tokenizer 精确估算
    • 否则 fallback：平均 1 token ≈ 4 字符
    """
    if tiktoken:
        enc = tiktoken.get_encoding("gpt2")
        return len(enc.encode(text))
    # 简易估算
    return len(text) // 4


# ─────────────────────────────── 主 调 用 ─────────────────────────────
def call_llm(
    prompt: str,
    *,
    use_cache: bool = True,
    model: str = DEFAULT_MODEL,
    max_chunk_size: int = DEFAULT_MAX_CHARS,
    _depth: int = 0,
) -> str:
    """
    调用 DeepSeek API；自动分块、递归聚合并加多重兜底。

    参数
    ----
    prompt : str
        要发送的完整提示。
    use_cache : bool
        是否启用本地 JSON 缓存。子块递归调用时会自动关闭。
    model : str
        DeepSeek 模型名。
    max_chunk_size : int
        单块最大字符数（注意不是 token）。
    _depth : int
        递归层计数（内部使用）。
    """
    # ——— 深度守卫 ———
    if _depth > MAX_RECURSION_DEPTH:
        raise RuntimeError("Exceeded maximum split depth; prompt may be pathological.")

    # ——— 缓存查找 ———
    if use_cache and (cached := _cache_get(prompt)):
        logger.debug("Returned cached response")
        return cached

    # ——— 长度检查 + 分块 ———
    if len(prompt) > max_chunk_size or estimate_token_count(prompt) > DEFAULT_MAX_CHARS:
        if _depth == 0:
            logger.info(
                "Prompt too long, splitting into chunks (max %s chars)",
                max_chunk_size,
            )

        chunks = split_prompt(prompt, max_chunk_size)

        # 双保险：如果奇怪格式仍只得到 1 个且超长 → 硬切
        if len(chunks) == 1 and len(chunks[0]) > max_chunk_size:
            chunks = _force_slice(prompt, max_chunk_size)

        responses = [
            call_llm(
                chunk,
                use_cache=False,  # 子块不写缓存
                model=model,
                max_chunk_size=max_chunk_size,
                _depth=_depth + 1,
            )
            for chunk in chunks
        ]
        full_resp = "\n\n".join(responses)
        _cache_set(prompt, full_resp, use_cache)
        return full_resp

    # ——— 走真正 API ———
    api_key = os.getenv("DEEPSEEK_API_KEY", "API_KEY")
    if not api_key:
        raise RuntimeError("Environment variable DEEPSEEK_API_KEY not set")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    try:
        logger.debug("Sending to DeepSeek (%s)…", model)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=DEFAULT_MAX_CHARS,
            temperature=0.3,
            timeout=1000,
        )
        answer = resp.choices[0].message.content.strip()
        _cache_set(prompt, answer, use_cache)  # 写缓存
        return answer

    except Exception as exc:  # noqa: WPS429
        # 针对性错误处理（可根据需求再细分）
        msg = str(exc)
        if "invalid_api_key" in msg:
            raise RuntimeError("Invalid DeepSeek API key") from exc
        if "rate_limit" in msg:
            raise RuntimeError("Hit DeepSeek rate limit; retry later") from exc
        if "context_length_exceeded" in msg or "exceeds" in msg:
            # 理论上不会走到这一步；如果真到了，就递归再缩
            logger.warning(
                "DeepSeek context length exceeded, retrying with tighter chunks"
            )
            return call_llm(
                prompt,
                use_cache=use_cache,
                model=model,
                max_chunk_size=int(max_chunk_size * 0.8),
                _depth=_depth + 1,
            )
        raise  # 其他未预料的直接抛出


# ──────────────────────────── 缓 存 辅 助 ────────────────────────────
def _cache_get(prompt: str) -> str | None:
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as fh:
            cache = json.load(fh)
        return cache.get(prompt)
    except Exception as exc:  # noqa: WPS429
        logger.warning("Cache load error: %s", exc)
        return None


def _cache_set(prompt: str, resp: str, enabled: bool = True) -> None:
    if not enabled or not resp.strip():
        return
    try:
        cache = {}
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as fh:
                cache = json.load(fh)
        cache[prompt] = resp
        with open(CACHE_FILE, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, indent=2, ensure_ascii=False)
    except Exception as exc:  # noqa: WPS429
        logger.error("Failed to save cache: %s", exc)


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
