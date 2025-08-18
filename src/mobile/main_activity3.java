package com.example.doomtrack;

import android.graphics.Bitmap;
import android.os.Bundle;

import androidx.activity.EdgeToEdge;
import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import android.os.Bundle;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.os.Message;
import androidx.webkit.WebViewAssetLoader;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import androidx.appcompat.app.AppCompatActivity;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;
import retrofit2.http.Body;
import retrofit2.http.Headers;
import retrofit2.http.POST;

public class MainActivity3 extends AppCompatActivity {

    private TextView outputBox;
    private EditText inputBox;
    private Button okButton;
    private WatsonApi watsonApi;
    WebView webView;

    public interface WatsonApi {
        @Headers({
                "Content-Type: application/json",
                "Authorization: Bearer wsoqlnGTLWhruMpvZmYJ86YH4MDsP0a60qnkZNeByLdl"
        })
        @POST("https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/d4fc2132-78e5-41cb-88a8-81a09b36faad/v1/agents/3ee75bd0-5c64-4078-9fb8-ccbdcbe76316/message")
        Call<WatsonResponse> sendMessage(@Body WatsonRequest request);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main3);

        webView = findViewById(R.id.webView);
//        webView.setWebChromeClient(new WebChromeClient());
//        webView.loadUrl("file:///Users/anishabinay/Documents/Terminal-Velocity/src/testing.html");
        webView.getSettings().setBuiltInZoomControls(true);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setAllowFileAccess(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        webView.getSettings().setJavaScriptCanOpenWindowsAutomatically(true);
        webView.getSettings().setAllowFileAccessFromFileURLs(true);
        webView.getSettings().setAllowUniversalAccessFromFileURLs(true);
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        //webView.setWebViewClient(new Callback());
        webView.loadUrl("file:///android_asset/index.html");
        //webView.loadUrl("https://ca-tor.watson-orchestrate.cloud.ibm.com/chat");


        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                view.loadUrl(url);
                return true;
            }

            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                super.onPageStarted(view, url, favicon);
                webView.setVisibility(View.GONE);
            }
            public void onBackPressed(){
                if(webView.canGoBack()) {
                    webView.goBack();
                }
            }
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                webView.setVisibility(View.VISIBLE);
            }
        });



    }






//        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
//            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
//            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
//            return insets;
//        });
//
//        outputBox = findViewById(R.id.outputBox);
//        inputBox = findViewById(R.id.inputBox);
//        okButton = findViewById(R.id.okButton);
//
//        Retrofit retrofit = new Retrofit.Builder()
//                .baseUrl("https://ca-tor.watson-orchestrate.cloud.ibm.com") // Watson base URL
//                .addConverterFactory(GsonConverterFactory.create())
//                .build();
//
//        watsonApi = retrofit.create(WatsonApi.class);
//        okButton.setOnClickListener(v -> {
//            String userInput = inputBox.getText().toString().trim();
//            if (!userInput.isEmpty()) {
//                // Append user's message
//                outputBox.append("\nYou: " + userInput);
//                inputBox.setText(""); // clear input
//
//                // Send to Watson
//                sendMessageToWatson(userInput);
//            }
//        });
//        }
//        private class Callback extends WebViewClient {
//            @Override
//            public boolean shouldOverrideUrlLoading(WebView view, String url){
//                return false;
//            }
//        }
////
//    public class WatsonRequest {
//        private String input;
//
//        public WatsonRequest(String input) {
//            this.input = input;
//        }
//
//        public String getInput() { return input; }
//        public void setInput(String input) { this.input = input; }
//    }
//
//    public class WatsonResponse {
//        private String output;
//
//        public String getOutput() { return output; }
//        public void setOutput(String output) { this.output = output; }
//    }
//    private void sendMessageToWatson(String message) {
//        WatsonRequest request = new WatsonRequest(message);
//
//        watsonApi.sendMessage(request).enqueue(new retrofit2.Callback<WatsonResponse>() {
//            @Override
//            public void onResponse(Call<WatsonResponse> call, Response<WatsonResponse> response) {
//                if(response.isSuccessful()){
//                    outputBox.append("\nReaches the agent");
//                    if (response.body() != null){
//                        outputBox.append("\nAI: " + response.body().getOutput());
//                    }
//                }
//                else{
//                    outputBox.append("\nCould not reach the agent");
//                }
//
//                /*if (response.isSuccessful() && response.body() != null) {
//                    outputBox.append("\nAI: " + response.body().getResponse());
//                } else {
//                    outputBox.append("\n[Error: No response from AI]");
//                }*/
//            }
//
//            @Override
//            public void onFailure(Call<WatsonResponse> call, Throwable t) {
//                Toast.makeText(MainActivity3.this, "Failed: " + t.getMessage(), Toast.LENGTH_SHORT).show();
//                outputBox.append("\n[Error: " + t.getMessage() + "]");
//            }
//        });
//    }
}
