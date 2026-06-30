package com.example.aiassistant

import com.example.aiassistant.RecommendationRequest
import com.example.aiassistant.RecommendationResponse

interface RecommendationRepository {
    suspend fun recommend(request: RecommendationRequest): RecommendationResponse
}

