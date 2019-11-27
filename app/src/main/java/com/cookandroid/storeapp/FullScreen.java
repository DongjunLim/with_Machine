package com.cookandroid.storeapp;


import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

import com.bumptech.glide.Glide;

public class FullScreen extends Activity {
    ImageView newimg;
    @Override
    protected void onCreate( Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.fullscreen);
        Intent intent=new Intent(this.getIntent());
        String s=intent.getStringExtra("text");
        newimg= (ImageView) findViewById(R.id.bigimageview);

        Glide.with(this).load(s).error(R.drawable.noimage).into(newimg);

        System.out.println(s);


    }
    public void onClick(View view){
        finish();
    }
}
