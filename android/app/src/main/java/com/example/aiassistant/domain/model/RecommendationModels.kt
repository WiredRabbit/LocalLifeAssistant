package com.example.aiassistant.domain.model

data class RecommendationRequest(
    val query: String,
    val city: String? = null,
    val limit: Int = 5
)

data class RecommendationResponse(
    val recommendations: List<RecommendationItem> = emptyList(),
    val summary: String = ""
)

data class RecommendationItem(
    val business_id: String,
    val name: String,
    val city: String?,
    val stars: Double?,
    val review_count: Int?,
    val address: String?,
    val categories: String?,
    val reason: String
)

