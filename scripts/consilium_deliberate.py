#!/usr/bin/env python3
"""
Consilium Deliberation Engine - Core deliberation script
为 AI 决策提供多方审议和安全审查
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from datetime import datetime


def load_api_key() -> str:
    """Load API key from environment variables."""
    return (
        os.getenv("DEEPSEEK_API_KEY") or 
        os.getenv("OPENAI_API_KEY") or 
        os.getenv("ANTHROPIC_API_KEY")
    )


def get_llm_backend() -> tuple[str, str, str]:
    """Determine which LLM backend to use based on available API keys."""
    if os.getenv("DEEPSEEK_API_KEY"):
        return (
            "deepseek",
            os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        )
    elif os.getenv("OPENAI_API_KEY"):
        return (
            "openai",
            "https://api.openai.com/v1",
            os.getenv("OPENAI_MODEL", "gpt-4")
        )
    elif os.getenv("ANTHROPIC_API_KEY"):
        return (
            "anthropic",
            "https://api.anthropic.com",
            os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        )
    else:
        raise ValueError("No API key found. Set DEEPSEEK_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")


def create_deliberation_prompt(requirement: str, context: Optional[Dict] = None) -> str:
    """Create the multi-party deliberation prompt."""
    
    safety_level = context.get("safety_level", "medium") if context else "medium"
    
    prompt = f"""你是一个多方审议决策引擎。请对以下需求进行多角色审议分析。

## 原始需求
{requirement}

## 审议流程

### 阶段 0: 多方审议
请模拟以下四个角色的讨论：

**产品经理 (PM)**
- 核心关注点：需求是否被准确理解？用户的真实意图是什么？
- 输出：需求澄清、边界定义

**技术负责人 (Tech Lead)**
- 核心关注点：技术方案是否可行？有什么技术风险？
- 输出：技术可行性分析、风险点

**成本专家 (Cost Expert)**
- 核心关注点：资源消耗如何？时间成本？API调用成本？
- 输出：成本估算、优化建议

**用户代表 (User Rep)**
- 核心关注点：从终端用户角度看，有什么潜在问题？体验如何？
- 输出：用户体验顾虑

### 阶段 1-5: 详细分析
基于上述讨论，生成：
1. **PRD** (需求文档) - 明确功能范围
2. **技术方案** - 实现方案概述
3. **成本分析** - 资源消耗明细
4. **风险评估** - 可能的风险和应对
5. **执行计划** - 步骤分解

### 阶段 6: 价值守护者审查 (安全级别: {safety_level})
请回答以下安全检查问题：
- 是否会泄露隐私数据？
- 是否会执行不可逆操作？
- 用户是否真正理解操作后果？
- 是否存在潜在的安全漏洞？

## 输出格式
请以JSON格式输出审议结果：

```json
{{
  "deliberation_summary": "审议总结（3-5句话）",
  "roles_analysis": {{
    "pm": {{
      "understanding": "PM对需求的理解",
      "clarifications": ["澄清点1", "澄清点2"],
      "concerns": ["顾虑1"]
    }},
    "tech_lead": {{
      "feasibility": "可行性评估",
      "approach": "推荐技术方案",
      "risks": ["风险1", "风险2"]
    }},
    "cost_expert": {{
      "estimate": "成本估算",
      "optimizations": ["优化建议1"]
    }},
    "user_rep": {{
      "experience_concerns": ["体验顾虑1"],
      "suggestions": ["建议1"]
    }}
  }},
  "deliverables": {{
    "prd": "需求文档摘要",
    "technical_proposal": "技术方案摘要",
    "cost_analysis": "成本分析摘要",
    "risk_assessment": "风险评估摘要",
    "execution_plan": ["步骤1", "步骤2", "步骤3"]
  }},
  "guardian_review": {{
    "privacy_risk": "隐私风险评估",
    "irreversible_ops": ["不可逆操作1"],
    "user_understanding": "用户理解度评估",
    "security_concerns": ["安全问题1"],
    "safety_level": "low|medium|high|critical"
  }},
  "decision_manifest": {{
    "approved_actions": ["可执行的操作1"],
    "needs_confirmation": ["需要确认的操作1"],
    "rejected_actions": ["拒绝执行的操作1"],
    "conditional_actions": ["带条件的操作1"],
    "safety_notes": ["安全提醒1"]
  }},
  "recommendation": "最终建议： proceed|proceed_with_caution|needs_clarification|reject"
}}
```

请确保输出是有效的JSON格式。"""
    
    return prompt


def call_llm(prompt: str, backend: str, base_url: str, model: str, api_key: str) -> str:
    """Call the LLM API with the given prompt."""
    
    try:
        if backend == "deepseek":
            return _call_deepseek(prompt, base_url, model, api_key)
        elif backend == "openai":
            return _call_openai(prompt, base_url, model, api_key)
        elif backend == "anthropic":
            return _call_anthropic(prompt, base_url, model, api_key)
        else:
            raise ValueError(f"Unknown backend: {backend}")
    except Exception as e:
        return json.dumps({
            "error": f"LLM API call failed: {str(e)}",
            "recommendation": "needs_clarification",
            "decision_manifest": {
                "approved_actions": [],
                "needs_confirmation": ["API调用失败，请检查配置后重试"],
                "rejected_actions": [],
                "safety_notes": ["建议手动检查API配置"]
            }
        }, ensure_ascii=False)


def _call_deepseek(prompt: str, base_url: str, model: str, api_key: str) -> str:
    """Call DeepSeek API."""
    import urllib.request
    import urllib.error
    
    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['choices'][0]['message']['content']


def _call_openai(prompt: str, base_url: str, model: str, api_key: str) -> str:
    """Call OpenAI API."""
    import urllib.request
    
    url = f"{base_url}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['choices'][0]['message']['content']


def _call_anthropic(prompt: str, base_url: str, model: str, api_key: str) -> str:
    """Call Anthropic Claude API."""
    import urllib.request
    
    url = f"{base_url}/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.3
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers=headers,
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        return result['content'][0]['text']


def extract_json_from_response(response: str) -> Dict[str, Any]:
    """Extract JSON from LLM response (handles markdown code blocks)."""
    import re
    
    # Try to find JSON in code blocks
    json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    matches = re.findall(json_pattern, response)
    
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue
    
    # Try to parse the entire response as JSON
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON-like structure
    try:
        start = response.find('{')
        end = response.rfind('}')
        if start != -1 and end != -1:
            return json.loads(response[start:end+1])
    except json.JSONDecodeError:
        pass
    
    # Return error response if all parsing fails
    return {
        "error": "Failed to parse JSON from LLM response",
        "raw_response": response[:500],
        "recommendation": "needs_clarification",
        "decision_manifest": {
            "approved_actions": [],
            "needs_confirmation": ["解析响应失败，请检查原始响应"],
            "rejected_actions": [],
            "safety_notes": ["建议手动审查原始响应"]
        }
    }


def format_output(result: Dict[str, Any], format_type: str = "markdown") -> str:
    """Format the deliberation result for display."""
    
    if format_type == "json":
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    # Markdown format
    lines = [
        "# 🧠 Consilium 审议报告",
        f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## 📋 审议总结\n{result.get('deliberation_summary', 'N/A')}",
        
        "\n## 👥 多方审议",
        "\n### 产品经理 (PM)",
        f"- **需求理解**: {result.get('roles_analysis', {}).get('pm', {}).get('understanding', 'N/A')}",
    ]
    
    pm_clarifications = result.get('roles_analysis', {}).get('pm', {}).get('clarifications', [])
    if pm_clarifications:
        lines.append(f"- **澄清点**: {', '.join(pm_clarifications)}")
    
    lines.extend([
        "\n### 技术负责人",
        f"- **可行性**: {result.get('roles_analysis', {}).get('tech_lead', {}).get('feasibility', 'N/A')}",
        f"- **推荐方案**: {result.get('roles_analysis', {}).get('tech_lead', {}).get('approach', 'N/A')}",
    ])
    
    tech_risks = result.get('roles_analysis', {}).get('tech_lead', {}).get('risks', [])
    if tech_risks:
        lines.append(f"- **风险**: {', '.join(tech_risks)}")
    
    lines.extend([
        "\n### 成本专家",
        f"- **成本估算**: {result.get('roles_analysis', {}).get('cost_expert', {}).get('estimate', 'N/A')}",
    ])
    
    cost_opts = result.get('roles_analysis', {}).get('cost_expert', {}).get('optimizations', [])
    if cost_opts:
        lines.append(f"- **优化建议**: {', '.join(cost_opts)}")
    
    lines.append("\n## 🛡️ 价值守护者审查")
    guardian = result.get('guardian_review', {})
    lines.extend([
        f"- **隐私风险**: {guardian.get('privacy_risk', 'N/A')}",
        f"- **用户理解度**: {guardian.get('user_understanding', 'N/A')}",
        f"- **安全级别**: {guardian.get('safety_level', 'unknown')}",
    ])
    
    irreversible = guardian.get('irreversible_ops', [])
    if irreversible:
        lines.append(f"- **⚠️ 不可逆操作**: {', '.join(irreversible)}")
    
    security = guardian.get('security_concerns', [])
    if security:
        lines.append(f"- **⚠️ 安全顾虑**: {', '.join(security)}")
    
    lines.append("\n## ✅ 决策清单")
    manifest = result.get('decision_manifest', {})
    
    approved = manifest.get('approved_actions', [])
    if approved:
        lines.append("\n### ✅ 批准执行")
        for action in approved:
            lines.append(f"- {action}")
    
    needs_conf = manifest.get('needs_confirmation', [])
    if needs_conf:
        lines.append("\n### ⚠️ 需要确认")
        for action in needs_conf:
            lines.append(f"- {action}")
    
    rejected = manifest.get('rejected_actions', [])
    if rejected:
        lines.append("\n### ❌ 拒绝执行")
        for action in rejected:
            lines.append(f"- {action}")
    
    safety_notes = manifest.get('safety_notes', [])
    if safety_notes:
        lines.append("\n### 📝 安全提醒")
        for note in safety_notes:
            lines.append(f"- {note}")
    
    recommendation = result.get('recommendation', 'unknown')
    emoji = {'proceed': '✅', 'proceed_with_caution': '⚠️', 'needs_clarification': '❓', 'reject': '❌'}
    lines.extend([
        "\n---",
        f"\n## 🎯 最终建议: {emoji.get(recommendation, '❓')} {recommendation}",
    ])
    
    return "\n".join(lines)


def deliberate(requirement: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Main entry point for Consilium deliberation.
    
    Args:
        requirement: The user requirement or task description
        context: Optional context dict with keys like safety_level, user_preferences, etc.
    
    Returns:
        Dict containing the full deliberation result
    """
    backend, base_url, model = get_llm_backend()
    api_key = load_api_key()
    
    prompt = create_deliberation_prompt(requirement, context)
    response = call_llm(prompt, backend, base_url, model, api_key)
    result = extract_json_from_response(response)
    
    # Add metadata
    result['_metadata'] = {
        'timestamp': datetime.now().isoformat(),
        'backend': backend,
        'model': model,
        'requirement': requirement
    }
    
    return result


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Consilium - Multi-Agent Collaborative Decision Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "自动回复所有邮件"
  %(prog)s "删除所有临时文件" --safety-level high
  %(prog)s "生成一个照片整理技能" --format json
        """
    )
    parser.add_argument('requirement', help='The requirement or task to deliberate')
    parser.add_argument('--safety-level', default='medium', 
                       choices=['low', 'medium', 'high', 'critical'],
                       help='Safety level for guardian review (default: medium)')
    parser.add_argument('--format', default='markdown', 
                       choices=['markdown', 'json'],
                       help='Output format (default: markdown)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    # Run deliberation
    context = {'safety_level': args.safety_level}
    result = deliberate(args.requirement, context)
    
    # Format output
    output = format_output(result, args.format)
    
    # Write output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report written to: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    # Return exit code based on recommendation
    recommendation = result.get('recommendation', 'needs_clarification')
    if recommendation == 'reject':
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
