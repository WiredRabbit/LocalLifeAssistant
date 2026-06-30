package com.example.aiassistant.ui

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aiassistant.data.ServiceLocator
import com.example.aiassistant.domain.model.RecommendationRequest
import com.example.aiassistant.domain.model.RecommendationResponse
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class RecommendationViewModel : ViewModel() {
    // UI state exposed as mutable properties to be observed by Compose
    var query by mutableStateOf("找一个安静、预算不超过 200 的餐厅")
    var city by mutableStateOf("Phoenix")
    var loading by mutableStateOf(false)
    var response by mutableStateOf<RecommendationResponse?>(null)
    var error by mutableStateOf<String?>(null)

    private val repository = ServiceLocator.provideRecommendationRepository()

    fun recommend(limit: Int = 5) {
        viewModelScope.launch {
            loading = true
            error = null
            try {
                val req = RecommendationRequest(query = query, city = city, limit = limit)
                val result = withContext(Dispatchers.IO) { repository.recommend(req) }
                response = result
            } catch (e: Exception) {
                error = e.message ?: "未知错误"
            } finally {
                loading = false
            }
        }
    }
}

