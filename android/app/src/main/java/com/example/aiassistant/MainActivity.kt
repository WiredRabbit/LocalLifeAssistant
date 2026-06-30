package com.example.aiassistant

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.material3.MaterialTheme
import androidx.activity.viewModels
import com.example.aiassistant.ui.RecommendationScreen
import com.example.aiassistant.ui.RecommendationViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: RecommendationViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MaterialTheme {
                RecommendationScreen(viewModel = viewModel)
            }
        }
    }
}

