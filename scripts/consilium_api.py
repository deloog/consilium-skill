#!/usr/bin/env python3
"""
Consilium API Module - Python API for integrating Consilium into applications
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class ConsiliumEngine:
    """
    Consilium决策引擎，提供多方审议和安全检查功能
    
    Usage:
        engine = ConsiliumEngine()
        result = engine.deliberate("自动回复所有邮件")
        
        # Execute approved actions only
        for action in result['decision_manifest']['approved_actions']:
            execute(action)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Consilium Engine.
        
        Args:
            config: Optional configuration dict with keys:
                - safety_level: 'low'|'medium'|'high'|'critical'
                - model: LLM model to use
                - backend: 'deepseek'|'openai'|'anthropic'
        """
        self.config = config or {}
        self.safety_level = self.config.get('safety_level', 'medium')
        self._load_backend()
    
    def _load_backend(self):
        """Load LLM backend configuration from environment."""
        if self.config.get('backend') == 'deepseek' or os.getenv('DEEPSEEK_API_KEY'):
            self.backend = 'deepseek'
            self.base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
            self.model = self.config.get('model') or os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
            self.api_key = os.getenv('DEEPSEEK_API_KEY')
        elif self.config.get('backend') == 'openai' or os.getenv('OPENAI_API_KEY'):
            self.backend = 'openai'
            self.base_url = 'https://api.openai.com/v1'
            self.model = self.config.get('model') or os.getenv('OPENAI_MODEL', 'gpt-4')
            self.api_key = os.getenv('OPENAI_API_KEY')
        elif self.config.get('backend') == 'anthropic' or os.getenv('ANTHROPIC_API_KEY'):
            self.backend = 'anthropic'
            self.base_url = 'https://api.anthropic.com'
            self.model = self.config.get('model') or os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-20250514')
            self.api_key = os.getenv('ANTHROPIC_API_KEY')
        else:
            raise ValueError("No API key found. Set DEEPSEEK_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")
    
    def deliberate(self, requirement: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Run full deliberation process on a requirement.
        
        Args:
            requirement: The requirement or task to analyze
            context: Additional context for deliberation
        
        Returns:
            Dict with deliberation results including decision_manifest
        """
        from .consilium_deliberate import create_deliberation_prompt, call_llm, extract_json_from_response
        
        ctx = context or {}
        ctx['safety_level'] = ctx.get('safety_level', self.safety_level)
        
        prompt = create_deliberation_prompt(requirement, ctx)
        response = call_llm(prompt, self.backend, self.base_url, self.model, self.api_key)
        result = extract_json_from_response(response)
        
        result['_metadata'] = {
            'timestamp': datetime.now().isoformat(),
            'backend': self.backend,
            'model': self.model,
            'requirement': requirement
        }
        
        return result
    
    def quick_check(self, action: str, action_type: str = 'general') -> Dict[str, Any]:
        """
        Quick safety check for a single action.
        
        Args:
            action: Description of the action to check
            action_type: Type of action ('file', 'network', 'data', 'general')
        
        Returns:
            Dict with safety assessment
        """
        prompts = {
            'file': f"检查文件操作的安全性: {action}",
            'network': f"检查网络操作的安全性: {action}",
            'data': f"检查数据处理操作的安全性: {action}",
            'general': f"检查以下操作的安全性: {action}"
        }
        
        return self.deliberate(prompts.get(action_type, prompts['general']))
    
    def review_skill(self, skill_code: str, skill_description: str) -> Dict[str, Any]:
        """
        Review a generated skill for quality and safety.
        
        Args:
            skill_code: The skill code to review
            skill_description: Description of what the skill does
        
        Returns:
            Dict with review results and suggestions
        """
        requirement = f"""审查以下技能的质量和安全性：

技能描述: {skill_description}

技能代码:
```python
{skill_code}
```

请评估：
1. 代码质量（可读性、健壮性）
2. 安全风险（是否有危险操作）
3. 功能完整性
4. 改进建议
"""
        return self.deliberate(requirement, {'safety_level': 'high'})
    
    def analyze_requirements(self, user_request: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Analyze and clarify complex user requirements.
        
        Args:
            user_request: The user's original request
            context: Additional context about the user/situation
        
        Returns:
            Dict with clarified requirements and recommendations
        """
        requirement = f"""分析并澄清以下用户需求：

用户请求: {user_request}

背景信息: {json.dumps(context or {}, ensure_ascii=False)}

请提供：
1. 用户真实意图分析
2. 明确的功能范围
3. 边界条件
4. 潜在的误解点
"""
        return self.deliberate(requirement, context)
    
    def is_safe_to_proceed(self, result: Dict[str, Any]) -> bool:
        """
        Check if deliberation result indicates it's safe to proceed.
        
        Args:
            result: The deliberation result dict
        
        Returns:
            True if safe to proceed, False otherwise
        """
        recommendation = result.get('recommendation', 'needs_clarification')
        return recommendation in ['proceed', 'proceed_with_caution']
    
    def get_approved_actions(self, result: Dict[str, Any]) -> List[str]:
        """
        Get list of approved actions from deliberation result.
        
        Args:
            result: The deliberation result dict
        
        Returns:
            List of approved action descriptions
        """
        return result.get('decision_manifest', {}).get('approved_actions', [])
    
    def get_risk_level(self, result: Dict[str, Any]) -> str:
        """
        Get the risk level from deliberation result.
        
        Args:
            result: The deliberation result dict
        
        Returns:
            Risk level string: 'low', 'medium', 'high', or 'critical'
        """
        return result.get('guardian_review', {}).get('safety_level', 'unknown')


# Convenience functions for direct use
def deliberate(requirement: str, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Convenience function for one-shot deliberation."""
    engine = ConsiliumEngine()
    return engine.deliberate(requirement, context)


def quick_safety_check(action: str) -> bool:
    """Quick check if an action is safe to proceed."""
    engine = ConsiliumEngine()
    result = engine.quick_check(action)
    return engine.is_safe_to_proceed(result)


def review_before_execute(action_description: str, callback=None):
    """
    Decorator/Context manager pattern for executing actions with review.
    
    Usage:
        def delete_files(pattern):
            # ... actual implementation
            pass
        
        # With review
        result = review_before_execute(
            f"Delete files matching: {pattern}",
            callback=lambda: delete_files(pattern)
        )
    """
    engine = ConsiliumEngine()
    result = engine.deliberate(action_description)
    
    if engine.is_safe_to_proceed(result):
        if callback:
            return callback()
        return {'proceed': True, 'result': result}
    else:
        return {
            'proceed': False,
            'reason': result.get('recommendation'),
            'concerns': result.get('decision_manifest', {}).get('needs_confirmation', []),
            'result': result
        }
