package com.example.aiassistant.data

import com.example.aiassistant.data.api.RecommendationApi
import com.example.aiassistant.data.repository.RecommendationRepositoryImpl
import com.example.aiassistant.RecommendationRepository
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ServiceLocator {
    private const val BASE_URL = "http://127.0.0.1:8002/"

    private val api: RecommendationApi by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(RecommendationApi::class.java)
    }

    fun provideRecommendationRepository(): RecommendationRepository {
        return RecommendationRepositoryImpl(api)
    }
}

