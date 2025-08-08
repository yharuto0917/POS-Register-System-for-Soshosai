# import src.api.api_gemini as getGeminiApiKey

"""
引数:
{
    "contents":{
        "model_name": "Gemini model name(ex: gemini-2.5-flash)",
        "prompt": "prompt for gemini",
        "materials": "materials for gemini"
    }
}
"""

import json
from google import genai
from src.api.api_gemini import getGeminiApiKey
from pydantic import BaseModel, Field
from typing import List
from enum import Enum

# Enumの定義
class TrendType(str, Enum):
    UP = "up"
    STABLE = "stable"
    DOWN = "down"

class InsightType(str, Enum):
    RECOMMENDATION = "recommendation"
    WARNING = "warning"
    OPPORTUNITY = "opportunity"

class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

# サブモデルの定義
class Period(BaseModel):
    """分析期間"""
    start: str = Field(..., description="分析開始日（YYYY-MM-DD形式）")
    end: str = Field(..., description="分析終了日（YYYY-MM-DD形式）")

class Metadata(BaseModel):
    """メタ情報"""
    analysisDate: str = Field(..., description="分析実行日（YYYY-MM-DD形式）")
    storeId: str = Field(..., description="店舗ID")
    period: Period = Field(..., description="分析対象期間")

class Metrics(BaseModel):
    """基本指標"""
    totalRevenue: int = Field(..., ge=0, description="総売上金額（円）")
    totalOrders: int = Field(..., ge=0, description="総注文数")
    averageOrderValue: int = Field(..., ge=0, description="平均客単価（円）")
    peakHour: str = Field(..., description="ピーク時間帯（例: 12:00-13:00）")
    growthRate: float = Field(..., description="前日比成長率（%）")

class TopProduct(BaseModel):
    """売上上位商品"""
    name: str = Field(..., description="商品名")
    revenue: int = Field(..., ge=0, description="売上金額（円）")
    quantity: int = Field(..., ge=0, description="販売数量")
    trend: TrendType = Field(..., description="売上トレンド")

class HourlyTrend(BaseModel):
    """時間帯別売上"""
    hour: str = Field(..., description="時間帯（例: 11:00-12:00）")
    revenue: int = Field(..., ge=0, description="売上金額（円）")
    orders: int = Field(..., ge=0, description="注文数")

class Insight(BaseModel):
    """重要な洞察"""
    type: InsightType = Field(..., description="洞察の種類")
    priority: Priority = Field(..., description="優先度")
    message: str = Field(..., max_length=100, description="洞察内容（100文字以内）")
    action: str = Field(..., max_length=50, description="推奨アクション（50文字以内）")

class Forecast(BaseModel):
    """明日の予測"""
    expectedRevenue: int = Field(..., ge=0, description="予想売上金額（円）")
    confidence: int = Field(..., ge=0, le=100, description="予測信頼度（0-100%）")
    recommendations: List[str] = Field(
        ..., 
        max_items=5,
        description="明日の準備推奨事項（最大5項目）"
    )

class AnalyzeResult(BaseModel):
    """売上分析結果"""
    metadata: Metadata = Field(..., description="分析メタ情報")
    metrics: Metrics = Field(..., description="基本指標")
    topProducts: List[TopProduct] = Field(
        ..., 
        min_items=1,
        max_items=5,
        description="売上TOP5商品"
    )
    hourlyTrend: List[HourlyTrend] = Field(
        ...,
        min_items=1,
        max_items=24,
        description="時間帯別売上トレンド"
    )
    insights: List[Insight] = Field(
        ...,
        min_items=1,
        max_items=3,
        description="重要な洞察（最大3つ）"
    )
    forecast: Forecast = Field(..., description="明日の予測")
    summary: str = Field(
        ...,
        max_length=100,
        description="1行サマリー（100文字以内）"
    )

class Config:
    # JSONスキーマ生成時の設定
    schema_extra = {
        "example": {
            "metadata": {
                "analysisDate": "2025-10-12",
                "storeId": "store001",
                "period": {
                    "start": "2025-10-11",
                    "end": "2025-10-12"
                }
            },
            "metrics": {
                "totalRevenue": 50000,
                "totalOrders": 120,
                "averageOrderValue": 417,
                "peakHour": "12:00-13:00",
                "growthRate": 15.5
            },
            "topProducts": [
                {
                    "name": "焼きそば",
                    "revenue": 15000,
                    "quantity": 50,
                    "trend": "up"
                }
            ],
            "hourlyTrend": [
                {
                    "hour": "11:00-12:00",
                    "revenue": 8000,
                    "orders": 20
                }
            ],
            "insights": [
                {
                    "type": "recommendation",
                    "priority": "high",
                    "message": "昼食時間帯の焼きそばが品薄。追加調理を推奨",
                    "action": "焼きそばを20食追加準備"
                }
            ],
            "forecast": {
                "expectedRevenue": 55000,
                "confidence": 75,
                "recommendations": [
                    "焼きそば60食準備",
                    "11時台のスタッフを1名増員"
                ]
            },
            "summary": "本日は昨日比15%増の好調。焼きそばの在庫に注意が必要。"
        }
    }

def geminiAnalyze(contents):
    try:
        # 入力データの検証
        if not isinstance(contents, dict):
            raise ValueError("contentsはdict形式である必要があります")
        
        # パラメータの取得
        model_name = contents.get("model_name")
        request_prompt = contents.get("prompt")
        request_materials = contents.get("materials")
        
        # 必須パラメータの検証
        if not model_name:
            raise ValueError("model_nameが指定されていません")
        if not request_prompt:
            raise ValueError("promptが指定されていません")
        if request_materials is None:
            raise ValueError("materialsが指定されていません")

        # Gemini APIキーの取得
        try:
            api_key = getGeminiApiKey()
            if api_key is None or api_key.strip() == "":
                raise ValueError("Gemini APIキーが設定されていません")
        except Exception as e:
            raise RuntimeError(f"APIキーの取得に失敗しました: {e}")

        # Geminiクライアントの初期化
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            raise RuntimeError(f"Geminiクライアントの初期化に失敗しました: {e}")

        # materialsをJSON文字列に変換（辞書の場合）
        try:
            if isinstance(request_materials, dict):
                materials_str = json.dumps(request_materials, ensure_ascii=False, indent=2)
            else:
                materials_str = str(request_materials)
        except Exception as e:
            raise ValueError(f"materialsの変換に失敗しました: {e}")

        prompt = f"role: you are a helpful assistant.You should answer the user\'s prompt based on the materials.\n\nuser_prompt: {request_prompt}\n\nmaterials: {materials_str}"

        # Gemini APIの呼び出し
        try:
            print(f"Gemini API呼び出し開始 - モデル: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema":AnalyzeResult
                }
            )
            
            if not response:
                raise ValueError("Gemini APIからの応答オブジェクトが空です")
            
            if not hasattr(response, 'text') or not response.text:
                raise ValueError("Gemini APIからの応答テキストが空です")
                
            print(f"Gemini API呼び出し成功 - レスポンス長: {len(response.text)}")
            return response.text
            
        except Exception as e:
            print(f"Gemini API呼び出しエラー: {type(e).__name__}: {e}")
            raise RuntimeError(f"Gemini API呼び出し中にエラーが発生しました: {type(e).__name__}: {e}")
        
    except ValueError as e:
        # 入力検証エラー
        raise ValueError(f"入力データエラー: {e}")
    except RuntimeError as e:
        # APIやネットワーク関連のエラー
        raise RuntimeError(f"実行時エラー: {e}")
    except Exception as e:
        # その他の予期しないエラー
        raise RuntimeError(f"予期しないエラーが発生しました: {e}")