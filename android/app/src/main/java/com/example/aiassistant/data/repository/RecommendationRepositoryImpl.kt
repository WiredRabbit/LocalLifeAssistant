package com.example.aiassistant.data.repository

import com.example.aiassistant.data.api.RecommendationApi
import com.example.aiassistant.RecommendationRequest
import com.example.aiassistant.RecommendationResponse
import com.example.aiassistant.RecommendationRepository

class RecommendationRepositoryImpl(
    private val api: RecommendationApi
) : RecommendationRepository {
    override suspend fun recommend(request: RecommendationRequest): RecommendationResponse {
        return api.recommend(request)
    }
}

