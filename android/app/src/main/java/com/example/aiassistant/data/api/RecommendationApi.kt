package com.example.aiassistant.data.api

import com.example.aiassistant.RecommendationRequest
import com.example.aiassistant.RecommendationResponse
import retrofit2.http.Body
import retrofit2.http.POST

interface RecommendationApi {
    @POST("/api/v1/recommendations")
    suspend fun recommend(@Body request: RecommendationRequest): RecommendationResponse
}

