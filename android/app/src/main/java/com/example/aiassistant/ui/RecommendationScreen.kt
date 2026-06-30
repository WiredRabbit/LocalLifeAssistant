package com.example.aiassistant.ui

import androidx.compose.foundation.layout.Column
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
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun RecommendationScreen(viewModel: RecommendationViewModel) {
    val query = viewModel.query
    val city = viewModel.city
    val loading = viewModel.loading
    val response = viewModel.response
    val error = viewModel.error

    Scaffold(modifier = Modifier.fillMaxSize()) { paddingValues ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            item {
                TextField(value = query, onValueChange = { viewModel.query = it }, label = { Text("查询") })
                TextField(value = city, onValueChange = { viewModel.city = it }, label = { Text("城市") })
                Button(onClick = { viewModel.recommend() }, modifier = Modifier.padding(top = 8.dp)) {
                    Text("推荐")
                }
                if (loading) {
                    CircularProgressIndicator(modifier = Modifier.padding(top = 8.dp))
                }
                error?.let { Text(it, modifier = Modifier.padding(top = 8.dp)) }
                response?.let { payload ->
                    Text(payload.summary, modifier = Modifier.padding(top = 8.dp))
                }
            }
            if (response != null) {
                items(response.recommendations) { item ->
                    Card(modifier = Modifier.padding(vertical = 8.dp)) {
                        Column(modifier = Modifier.padding(12.dp)) {
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


