package com.example.aiassistant

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.POST

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialTheme {
                RecommendationScreen()
            }
        }
    }
}

interface RecommendationApi {
    @POST("/api/v1/recommendations")
    suspend fun recommend(@Body request: RecommendationRequest): RecommendationResponse
}

data class RecommendationRequest(
    val query: String,
    val city: String? = null,
    val limit: Int = 5
)

data class RecommendationResponse(
    val recommendations: List<RecommendationItem>,
    val summary: String
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

@Composable
fun RecommendationScreen() {
    var query by remember { mutableStateOf("找一个安静、预算不超过 200 的餐厅") }
    var city by remember { mutableStateOf("Phoenix") }
    var loading by remember { mutableStateOf(false) }
    var response by remember { mutableStateOf<RecommendationResponse?>(null) }
    var error by remember { mutableStateOf<String?>(null) }

    val api = remember {
        Retrofit.Builder()
            .baseUrl("http://127.0.0.1:8002/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(RecommendationApi::class.java)
    }

    Scaffold(modifier = Modifier.fillMaxSize()) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            item {
                TextField(value = query, onValueChange = { query = it }, label = { Text("查询") })
                TextField(value = city, onValueChange = { city = it }, label = { Text("城市") })
                Button(onClick = {
                    loading = true
                    error = null
                    CoroutineScope(Dispatchers.IO).launch {
                        try {
                            val result = api.recommend(RecommendationRequest(query = query, city = city, limit = 5))
                            CoroutineScope(Dispatchers.Main).launch {
                                response = result
                                loading = false
                            }
                        } catch (e: Exception) {
                            CoroutineScope(Dispatchers.Main).launch {
                                error = e.message
                                loading = false
                            }
                        }
                    }
                }) {
                    Text("推荐")
                }
                if (loading) {
                    CircularProgressIndicator()
                }
                error?.let { Text(it) }
                response?.let { payload ->
                    Text(payload.summary)
                }
            }
            if (response != null) {
                items(response!!.recommendations) { item ->
                    Card(modifier = Modifier.padding(vertical = 8.dp)) {
                        androidx.compose.foundation.layout.Column(modifier = Modifier.padding(12.dp)) {
                            Text(item.name, style = MaterialTheme.typography.titleMedium)
                            Text("评分: ${item.stars ?: "-"}")
                            Text("评论数: ${item.review_count ?: "-"}")
                            Text("地址: ${item.address ?: "-"}")
                            Text("类别: ${item.categories ?: "-"}")
                            Text("原因: ${item.reason}")
                        }
                    }
                }
            }
        }
    }
}
