package com.example.aiassistant.domain.repository

import com.example.aiassistant.domain.model.RecommendationRequest
import com.example.aiassistant.domain.model.RecommendationResponse

interface RecommendationRepository {
    suspend fun recommend(request: RecommendationRequest): RecommendationResponse
}
