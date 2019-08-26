package com.cookandroid.storeapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.RatingBar;
import android.widget.ScrollView;
import android.widget.TextView;
import com.android.volley.RequestQueue;

import androidx.appcompat.app.AppCompatActivity;
import androidx.viewpager.widget.ViewPager;

public class InfoActivity extends AppCompatActivity {
    ImageAdapter adapter;
    ViewPager viewPager;
    LinearLayout layout1;
    Button backButton;
    ScrollView scrollView1, scrollView2;
    TextView name, formatted_address, price_level, tv1, text1, phone;
    RatingBar rating;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initView();
        String storeName, address, phoneNum, authorName, text;
        Double price, ratingBar;

        Intent intent = getIntent(); /*데이터 수신*/

        scrollView2.setOnTouchListener(new View.OnTouchListener() {
            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if(event.getAction() == MotionEvent.ACTION_UP) {
                    scrollView1.requestDisallowInterceptTouchEvent(false);
                }
                else {
                    scrollView1.requestDisallowInterceptTouchEvent(true);
                }
                return false;
            }
        });

        storeName = intent.getExtras().getString("name"); /*String형*/
        address = intent.getExtras().getString("address"); /*String형*/
        price = intent.getExtras().getDouble("price"); /*String형*/
        ratingBar = intent.getExtras().getDouble("ratingBar"); /*String형*/
        phoneNum = intent.getExtras().getString("phoneNum"); /*String형*/
        name.setText(storeName);
        formatted_address.setText(address);
        price_level.setText(price.toString());
        rating.setRating(Float.parseFloat(ratingBar.toString()));
        phone.setText(phoneNum);
        for(int i=0; i<5; i++) {
            authorName = intent.getExtras().getString("authorName"+i); /*String형*/
            text = intent.getExtras().getString("text"+i); /*String형*/
            text1.setText(text1.getText()+authorName+":\n"+text+"\n\n");
        }

    }

    public void initView() {
        viewPager = (ViewPager) findViewById(R.id.view);
        adapter = new ImageAdapter(this);
        viewPager.setAdapter(adapter);
        layout1 = (LinearLayout)findViewById(R.id.backgroundlayout);
        backButton = (Button)findViewById(R.id.backButton);
        scrollView1 = (ScrollView)findViewById(R.id.scrollView1);
        scrollView2 = (ScrollView)findViewById(R.id.scrollView2);

        tv1=(TextView)findViewById(R.id.text1);
        name=(TextView)findViewById(R.id.name);
        formatted_address=(TextView)findViewById(R.id.formatted_address);
        price_level=(TextView)findViewById(R.id.price_level);
        text1 = (TextView)findViewById(R.id.text1);
        rating = (RatingBar)findViewById(R.id.rating);
        phone = (TextView)findViewById(R.id.phone);
    }


}
