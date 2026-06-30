package com.example.aiassistant.data.repository

import com.example.aiassistant.data.api.RecommendationApi
import com.example.aiassistant.domain.model.RecommendationRequest
import com.example.aiassistant.domain.model.RecommendationResponse
import com.example.aiassistant.domain.repository.RecommendationRepository

class RecommendationRepositoryImpl(
    private val api: RecommendationApi
) : RecommendationRepository {
    override suspend fun recommend(request: RecommendationRequest): RecommendationResponse {
        return api.recommend(request)
    }
}

