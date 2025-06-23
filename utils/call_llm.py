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
from collections import deque
from typing import List

from openai import OpenAI

try:
    import tiktoken  # type: ignore
except ImportError:  # pragma: no cover
    tiktoken = None

__all__ = [
    "call_llm",
    "DEFAULT_MODEL",
    "DEFAULT_MAX_CHARS",
    "MAX_RECURSION_DEPTH",
]

# ────────────────────────────── Configuration ──────────────────────────────

DEFAULT_MAX_CHARS: int = 13_000  # single OpenAI request budget (≈ tokens)
DEFAULT_MODEL: str = "<model_name>"  # e.g., "deepseek-r1:latest"
BASE_URL: str = "<api_base_url>"  # e.g., "http://192.168.1.5:12345/v1"
CACHE_FILE: str = "llm_cache.json"
MAX_RECURSION_DEPTH: int = 100  # logical depth, *not* call‑stack depth

# ───────────────────────────────── Logging ─────────────────────────────────

logger = logging.getLogger(__name__)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter("[%(levelname)s %(asctime)s] %(message)s", "%H:%M:%S")
    )
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
logger.propagate = False

# ─────────────────────────── Utility helpers ───────────────────────────────


def _force_slice(text: str, max_size: int) -> list[str]:
    """Hard‑slice *text* into ≤ *max_size* char chunks (final fallback)."""
    return [text[i : i + max_size] for i in range(0, len(text), max_size)]  # noqa: E203


def split_prompt(prompt: str, max_size: int = DEFAULT_MAX_CHARS) -> list[str]:
    """Heuristic splitter (file ➜ class/def ➜ line). Ensures each piece ≤ *max_size*."""

    # ① File‑level diff markers
    file_sections = re.split(r"(?=File:\s+)", prompt)
    if len(file_sections) > 1:
        return _smart_concat(file_sections, max_size)

    # ② class / def boundaries – **regex fixed here**
    class_sections = re.split(r"(?=class\s+\w+\s*:|def\s+\w+\(\))", prompt)
    if len(class_sections) > 1:
        return _smart_concat(class_sections, max_size)

    # ③ Fallback – by lines
    return _smart_concat(prompt.splitlines(keepends=True), max_size)


def _smart_concat(sections: list[str], max_size: int) -> list[str]:
    """Greedily concatenate *sections* into chunks ≤ *max_size* chars."""
    chunks: list[str] = []
    current = ""
    for sec in sections:
        if not sec:
            continue
        # If a *single* section is still too big, slice it hard
        if len(sec) > max_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_force_slice(sec, max_size))
            continue

        if len(current) + len(sec) > max_size:
            chunks.append(current)
            current = sec
        else:
            current += sec
    if current:
        chunks.append(current)
    return chunks


def estimate_token_count(text: str) -> int:
    if tiktoken:
        enc = tiktoken.get_encoding("gpt2")
        return len(enc.encode(text))
    # naive fallback: 1 token ≈ 4 chars
    return len(text) // 4


# ───────────────────────────── Cache helpers ───────────────────────────────


def _cache_get(prompt: str) -> str | None:
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as fh:
            cache: dict[str, str] = json.load(fh)
        return cache.get(prompt)
    except Exception as exc:  # pragma: no cover
        logger.warning("Cache load error: %s", exc)
        return None


def _cache_set(prompt: str, resp: str, *, enabled: bool = True) -> None:
    if not enabled or not resp.strip():
        return
    cache: dict[str, str] = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as fh:
                cache = json.load(fh)
        except Exception as exc:  # pragma: no cover
            logger.warning("Cache read error: %s", exc)
    cache[prompt] = resp
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False, indent=2)
    except Exception as exc:  # pragma: no cover
        logger.error("Cache write error: %s", exc)


# ────────────────────────── Internal split routine ─────────────────────────


def _split_to_chunks(
    text: str,
    *,
    max_size: int,
    max_depth: int = MAX_RECURSION_DEPTH,
) -> list[str]:
    """Breadth‑first splitting without recursive call‑stack growth."""
    from collections import deque

    queue: deque[tuple[str, int]] = deque([(text, 0)])
    result: list[str] = []

    while queue:
        current, depth = queue.popleft()

        # char / token guard – split?
        if (
            len(current) <= max_size
            and estimate_token_count(current) <= DEFAULT_MAX_CHARS
        ):
            result.append(current)
            continue

        if depth >= max_depth:
            logger.warning("Depth %s reached; force‑slicing remaining text", depth)
            result.extend(_force_slice(current, max_size))
            continue

        subs = split_prompt(current, max_size)
        if len(subs) == 1 and len(subs[0]) == len(current):
            subs = _force_slice(current, max_size)
        queue.extend((s, depth + 1) for s in subs)

    return result


# ───────────────────────────── API interaction ─────────────────────────────


def _send_to_deepseek(prompt: str, model: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-b6675fce3b704310bbdbe9946da77530")
    if not api_key:
        raise RuntimeError("Environment variable DEEPSEEK_API_KEY not set")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    logger.debug(
        "[DeepSeek] → %s | %s chars (%s tokens)",
        model,
        len(prompt),
        estimate_token_count(prompt),
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=DEFAULT_MAX_CHARS,
        temperature=0.3,
        timeout=1000,
    )
    return resp.choices[0].message.content.strip()


# ──────────────────────────── Public entrypoint ────────────────────────────


def call_llm(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_chunk_size: int = DEFAULT_MAX_CHARS,
    use_cache: bool = True,
) -> str:
    """High‑level helper that transparently splits, caches and stitches."""

    cached = _cache_get(prompt) if use_cache else None
    if cached is not None:
        logger.debug("Returned cached response")
        return cached

    chunks = _split_to_chunks(prompt, max_size=max_chunk_size)
    if len(chunks) > 1:
        logger.info("Prompt split into %s chunks", len(chunks))

    responses: list[str] = []
    for idx, chunk in enumerate(chunks, 1):
        cached_piece = _cache_get(chunk) if use_cache else None
        if cached_piece is None:
            logger.info("Calling DeepSeek [%s/%s]…", idx, len(chunks))
            piece = _send_to_deepseek(chunk, model)
            _cache_set(chunk, piece, enabled=use_cache)
        else:
            logger.debug("Using cached piece [%s/%s]", idx, len(chunks))
            piece = cached_piece
        responses.append(piece)

    full_resp = "\n\n".join(responses)
    _cache_set(prompt, full_resp, enabled=use_cache)
    return full_resp


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
import json
import logging
import os
import re
from collections import deque
from typing import List

from openai import OpenAI

try:
    import tiktoken  # type: ignore
except ImportError:  # pragma: no cover
    tiktoken = None

__all__ = [
    "call_llm",
    "DEFAULT_MODEL",
    "DEFAULT_MAX_CHARS",
    "MAX_RECURSION_DEPTH",
]

# ────────────────────────────── Configuration ──────────────────────────────

DEFAULT_MAX_CHARS: int = 13_000  # single OpenAI request budget (≈ tokens)
DEFAULT_MODEL: str = "deepseek-r1:latest"
BASE_URL: str = "http://5j44925h56.oicp.vip:9434/v1"
# DEFAULT_MODEL: str = "deepseek-r1-distill-qwen-14b"
# BASE_URL: str = "http://localhost:12345/v1"
CACHE_FILE: str = "llm_cache.json"
MAX_RECURSION_DEPTH: int = 100  # logical depth, *not* call‑stack depth

# ───────────────────────────────── Logging ─────────────────────────────────

logger = logging.getLogger(__name__)
if not logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(
        logging.Formatter("[%(levelname)s %(asctime)s] %(message)s", "%H:%M:%S")
    )
    logger.addHandler(_handler)
    logger.setLevel(logging.INFO)
logger.propagate = False

# ─────────────────────────── Utility helpers ───────────────────────────────


def _force_slice(text: str, max_size: int) -> list[str]:
    """Hard‑slice *text* into ≤ *max_size* char chunks (final fallback)."""
    return [text[i : i + max_size] for i in range(0, len(text), max_size)]  # noqa: E203


def split_prompt(prompt: str, max_size: int = DEFAULT_MAX_CHARS) -> list[str]:
    """Heuristic splitter (file ➜ class/def ➜ line). Ensures each piece ≤ *max_size*."""

    # ① File‑level diff markers
    file_sections = re.split(r"(?=File:\s+)", prompt)
    if len(file_sections) > 1:
        return _smart_concat(file_sections, max_size)

    # ② class / def boundaries – **regex fixed here**
    class_sections = re.split(r"(?=class\s+\w+\s*:|def\s+\w+\(\))", prompt)
    if len(class_sections) > 1:
        return _smart_concat(class_sections, max_size)

    # ③ Fallback – by lines
    return _smart_concat(prompt.splitlines(keepends=True), max_size)


def _smart_concat(sections: list[str], max_size: int) -> list[str]:
    """Greedily concatenate *sections* into chunks ≤ *max_size* chars."""
    chunks: list[str] = []
    current = ""
    for sec in sections:
        if not sec:
            continue
        # If a *single* section is still too big, slice it hard
        if len(sec) > max_size:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(_force_slice(sec, max_size))
            continue

        if len(current) + len(sec) > max_size:
            chunks.append(current)
            current = sec
        else:
            current += sec
    if current:
        chunks.append(current)
    return chunks


def estimate_token_count(text: str) -> int:
    if tiktoken:
        enc = tiktoken.get_encoding("gpt2")
        return len(enc.encode(text))
    # naive fallback: 1 token ≈ 4 chars
    return len(text) // 4


# ───────────────────────────── Cache helpers ───────────────────────────────


def _cache_get(prompt: str) -> str | None:
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as fh:
            cache: dict[str, str] = json.load(fh)
        return cache.get(prompt)
    except Exception as exc:  # pragma: no cover
        logger.warning("Cache load error: %s", exc)
        return None


def _cache_set(prompt: str, resp: str, *, enabled: bool = True) -> None:
    if not enabled or not resp.strip():
        return
    cache: dict[str, str] = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as fh:
                cache = json.load(fh)
        except Exception as exc:  # pragma: no cover
            logger.warning("Cache read error: %s", exc)
    cache[prompt] = resp
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as fh:
            json.dump(cache, fh, ensure_ascii=False, indent=2)
    except Exception as exc:  # pragma: no cover
        logger.error("Cache write error: %s", exc)


# ────────────────────────── Internal split routine ─────────────────────────


def _split_to_chunks(
    text: str,
    *,
    max_size: int,
    max_depth: int = MAX_RECURSION_DEPTH,
) -> list[str]:
    """Breadth‑first splitting without recursive call‑stack growth."""
    from collections import deque

    queue: deque[tuple[str, int]] = deque([(text, 0)])
    result: list[str] = []

    while queue:
        current, depth = queue.popleft()

        # char / token guard – split?
        if (
            len(current) <= max_size
            and estimate_token_count(current) <= DEFAULT_MAX_CHARS
        ):
            result.append(current)
            continue

        if depth >= max_depth:
            logger.warning("Depth %s reached; force‑slicing remaining text", depth)
            result.extend(_force_slice(current, max_size))
            continue

        subs = split_prompt(current, max_size)
        if len(subs) == 1 and len(subs[0]) == len(current):
            subs = _force_slice(current, max_size)
        queue.extend((s, depth + 1) for s in subs)

    return result


# ───────────────────────────── API interaction ─────────────────────────────


def _send_to_deepseek(prompt: str, model: str) -> str:
    api_key = os.getenv("DEEPSEEK_API_KEY", "sk-b6675fce3b704310bbdbe9946da77530")
    if not api_key:
        raise RuntimeError("Environment variable DEEPSEEK_API_KEY not set")

    client = OpenAI(api_key=api_key, base_url=BASE_URL)
    logger.debug(
        "[DeepSeek] → %s | %s chars (%s tokens)",
        model,
        len(prompt),
        estimate_token_count(prompt),
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=DEFAULT_MAX_CHARS,
        temperature=0.3,
        timeout=1000,
    )
    return resp.choices[0].message.content.strip()


# ──────────────────────────── Public entrypoint ────────────────────────────


def call_llm(
    prompt: str,
    *,
    model: str = DEFAULT_MODEL,
    max_chunk_size: int = DEFAULT_MAX_CHARS,
    use_cache: bool = True,
) -> str:
    """High‑level helper that transparently splits, caches and stitches."""

    cached = _cache_get(prompt) if use_cache else None
    if cached is not None:
        logger.debug("Returned cached response")
        return cached

    chunks = _split_to_chunks(prompt, max_size=max_chunk_size)
    if len(chunks) > 1:
        logger.info("Prompt split into %s chunks", len(chunks))

    responses: list[str] = []
    for idx, chunk in enumerate(chunks, 1):
        cached_piece = _cache_get(chunk) if use_cache else None
        if cached_piece is None:
            logger.info("Calling DeepSeek [%s/%s]…", idx, len(chunks))
            piece = _send_to_deepseek(chunk, model)
            _cache_set(chunk, piece, enabled=use_cache)
        else:
            logger.debug("Using cached piece [%s/%s]", idx, len(chunks))
            piece = cached_piece
        responses.append(piece)

    full_resp = "\n\n".join(responses)
    _cache_set(prompt, full_resp, enabled=use_cache)
    return full_resp


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")


if __name__ == "__main__":
    test_prompt = "Hello, how are you?"

    # First call - should hit the API
    print("Making call...")
    response1 = call_llm(test_prompt, use_cache=False)
    print(f"Response: {response1}")
