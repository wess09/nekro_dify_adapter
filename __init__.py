import json
import aiohttp
from typing import Dict, Any, Optional, List
from nekro_agent.api.plugin import NekroPlugin, SandboxMethodType
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.api import core

# 创建插件实例
plugin = NekroPlugin(
    name="NekroDify",
    module_name="dify_adapter",
    description="通过Dify API调用 Dify工作流 的插件",
    author="wess09",
    version="1.0.2",
    url="https://github.com/wess09/nekro_plugin_dify"
)

# 添加插件配置
from nekro_agent.api.plugin import ConfigBase
from pydantic import Field

@plugin.mount_config()
class DifyConfig(ConfigBase):
    """Dify适配器配置"""
    
    api_key: str = Field(
        default="",
        title="Dify API密钥",
        description="Dify API密钥，格式为 app-xxxxxxxx",
        json_schema_extra={"required": True}
    )
    
    base_url: str = Field(
        default="https://api.dify.ai/v1",
        title="Dify API基础URL",
        description="Dify API基础URL"
    )
    
    default_user: str = Field(
        default="nekro-agent-user",
        title="默认用户标识",
        description="默认用户标识"
    )
    
    tip: str = Field(
        default="此项无需填写仅为提示作用",
        title="请在人设市场获取Dify工具描述格式，并添加到您的人设中",
        description="请在人设市场获取Dify工具描述格式，并添加到您的人设中"
    )

class DifyAPIClient:
    """Dify API客户端"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def run_workflow(self, inputs: Dict[str, Any], user: str = "nekro-user") -> Dict[str, Any]:
        """执行workflow（仅阻塞模式）"""
        url = f"{self.base_url}/workflows/run"
        data = {
            "inputs": inputs,
            "response_mode": "blocking",
            "user": user
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Dify API调用失败 (状态码: {response.status}): {error_text}")
    



def get_dify_client() -> DifyAPIClient:
    """获取配置好的Dify客户端"""
    config = plugin.get_config(DifyConfig)
    if not config.api_key:
        raise ValueError("请先配置Dify API密钥")
    return DifyAPIClient(config.api_key, config.base_url)



@plugin.mount_sandbox_method(
    method_type=SandboxMethodType.AGENT,
    name="run_dify_workflow",
    description="执行Dify工作流"
)
async def run_dify_workflow(_ctx: AgentCtx, inputs: Dict[str, Any], user: Optional[str] = None) -> str:
    """执行Dify工作流
    
    Args:
        inputs (Dict[str, Any]): 工作流输入参数，键值对格式
        user (Optional[str]): 用户标识，如果不提供则使用配置中的默认用户
    
    Returns:
        str: 工作流执行结果的描述
    
    Raises:
        Exception: 当API调用失败时抛出异常
    """
    try:
        client = get_dify_client()
        config = plugin.get_config(DifyConfig)
        
        if user is None:
            user = config.default_user
        
        core.logger.info(f"执行Dify工作流，输入参数: {inputs}")
        
        result = await client.run_workflow(inputs, user)
        
        core.logger.success(f"Dify工作流执行成功，结果: {result}")
        
        # 将结果转换为字符串描述，供AI进一步处理
        if isinstance(result, dict):
            if 'data' in result:
                # 如果结果包含data字段，提取其中的内容
                data = result['data']
                if isinstance(data, dict) and 'outputs' in data:
                    outputs = data['outputs']
                    return f"Dify工作流执行成功。输出结果：{json.dumps(outputs, ensure_ascii=False, indent=2)}"
                else:
                    return f"Dify工作流执行成功。结果数据：{json.dumps(data, ensure_ascii=False, indent=2)}"
            else:
                return f"Dify工作流执行成功。完整结果：{json.dumps(result, ensure_ascii=False, indent=2)}"
        else:
            return f"Dify工作流执行成功。结果：{str(result)}"
        
    except Exception as e:
        core.logger.error(f"执行Dify工作流失败: {e}")
        return f"Dify工作流执行失败：{str(e)}"





@plugin.mount_init_method()
async def initialize_plugin():
    """插件初始化"""
    core.logger.info(f"插件 '{plugin.name}' 正在初始化...")
    
    # 检查配置
    try:
        config = plugin.get_config(DifyConfig)
        if config.api_key:
            core.logger.info("Dify API密钥已配置")
        else:
            core.logger.warning("Dify API密钥未配置，请在插件配置中设置")
    except Exception as e:
        core.logger.warning(f"获取插件配置时出错: {e}")
    
    core.logger.success(f"插件 '{plugin.name}' 初始化完成")


@plugin.mount_cleanup_method()
async def cleanup_plugin():
    """插件清理"""
    core.logger.info(f"插件 '{plugin.name}' 正在清理...")
    # 这里可以添加清理逻辑，比如关闭连接等
    core.logger.success(f"插件 '{plugin.name}' 清理完成")