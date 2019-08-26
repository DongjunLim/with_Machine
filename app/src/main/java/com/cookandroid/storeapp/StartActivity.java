package com.cookandroid.storeapp;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import androidx.appcompat.app.AppCompatActivity;

public class StartActivity extends AppCompatActivity {

    RadioGroup radioGroup, radioGroup2;
    RadioButton korean, korea;
    Button okButton;
    public static String lang, country;

    public static Context mContext;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.second);


        radioGroup = findViewById(R.id.radioGroup);
        radioGroup2 = findViewById(R.id.radioGroup2);
        mContext = this;

        korean = findViewById(R.id.korean);
        korean.setChecked(true);
        korea = findViewById(R.id.korea);
        korea.setChecked(true);

        okButton = (findViewById(R.id.okButton));
        okButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int rb = radioGroup.getCheckedRadioButtonId();
                int rb2 = radioGroup2.getCheckedRadioButtonId();

                switch (rb) {
                    case R.id.korean: {
                        lang = "ko";
                        break;
                    }
                    case R.id.english: {
                        lang = "en";
                        break;
                    }
                    case R.id.chinese: {
                        lang = "zh-CN";
                        break;
                    }
                    case R.id.japanese: {
                        lang = "ja";
                        break;
                    }
                    case R.id.franch: {
                        lang = "fr";
                        break;
                    }
                    case R.id.spanish: {
                        lang = "es";
                        break;
                    }
                    case R.id.vietnamese: {
                        lang = "vi";
                        break;
                    }
                    case R.id.german: {
                        lang = "de";
                        break;
                    }

                }

                switch (rb2) {
                    case R.id.korea: {
                        country = "ko";
                        break;
                    }
                    case R.id.english_speaking: {
                        country = "en";
                        break;
                    }
                    case R.id.china: {
                        country = "zh-CN";
                        break;
                    }
                    case R.id.japan: {
                        country = "ja";
                        break;
                    }
                    case R.id.france: {
                        country = "fr";
                        break;
                    }
                    case R.id.spain: {
                        country = "es";
                        break;
                    }
                    case R.id.vietnam: {
                        country = "vi";
                        break;
                    }
                    case R.id.germany: {
                        country = "de";
                        break;
                    }
                }
                Intent intent = new Intent(getApplicationContext(), CameraActivity.class);
                startActivity(intent);
            }
        });

    }
}
