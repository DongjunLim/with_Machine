package com.cookandroid.storeapp;

import android.Manifest;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.start);

        Handler handler = new Handler(){
            public void handleMessage(Message msg) {
                super.handleMessage(msg);
                startActivity(new Intent(MainActivity.this, StartActivity.class));
                finish();
            }
        };
        handler.sendEmptyMessageDelayed(0, 1500);

    }
}
