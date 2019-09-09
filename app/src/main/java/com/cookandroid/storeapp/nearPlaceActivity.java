package com.cookandroid.storeapp;

import android.content.Context;
import android.content.Intent;
import android.location.LocationManager;
import android.os.Bundle;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

import androidx.appcompat.app.AppCompatActivity;

public class nearPlaceActivity extends AppCompatActivity {
    private String lang, country;
    private RequestQueue requestQueue;
    public double longitude, latitude;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.wait);

        Intent intent = getIntent(); /*데이터 수신*/
        String name = intent.getExtras().getString("storename");
        String position = intent.getExtras().getString("position");
        lang = ((StartActivity)StartActivity.mContext).lang;
        country = ((StartActivity)StartActivity.mContext).country;

        String result1 = position.split(",")[0];
        String result2 = position.split(",")[1];
        String result3 = result1.replace("(","");

        latitude = Double.parseDouble(result3.split(" ")[1]);
        longitude = Double.parseDouble(result2.replace(")",""));


        System.out.println("latitude : "+latitude+", longitude : "+longitude);
        String re_response = name.toLowerCase();
        re_response = re_response.replace("\n", "").replace("\r", "");

        String data = "{"+
                "\"user_language\"" + ": "+"\"" + lang + "\","+"\n"+
                "\"visit_language\"" + ": "+"\"" + country + "\","+"\n"+
                "\"store_name\"" + ": "+"\"" + re_response + "\","+"\n"+
                "\"gps_lat\"" + ":" + latitude + ","+
                "\"gps_lon\"" + ":" + longitude +
                "}";
        System.out.print("서버에 전달되는 데이터 \n"+data);
        //tv.setText("서버에 전달되는 데이터 \n"+data+"\n\n");

        Submit(data);
    }
    private void Submit(String data) {
        final String savedata = data;
        String URL = "http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/data";

        requestQueue = Volley.newRequestQueue(getApplicationContext());
        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
            //통신 성공 시
            @Override
            public void onResponse(String response) {
                // json 파싱
                try {
                    JSONObject object = new JSONObject(response);
                    // 응답 안 result 태그

                    // result 바로 밑 태그들
                    String address= object.getString("formatted_address");
                    String storeName = object.getString("name");
                    Double price = object.getDouble("price_level");
                    Double ratingBar = object.getDouble("rating");
                    String phoneNum = object.getString("phone");
                    String types =  object.getString("types");

                    // result의 reviews 태그 안 내용들
                    String reviews = object.getString("reviews");
                    JSONArray reviewArray = new JSONArray(reviews);

                    Intent intent = new Intent(getApplicationContext(), InfoActivity.class);
                    intent.putExtra("name", storeName);
                    System.out.println("매장이름:"+storeName);
                    intent.putExtra("address", address);
                    intent.putExtra("price", price);
                    intent.putExtra("ratingBar", ratingBar);
                    intent.putExtra("phoneNum", phoneNum);
                    intent.putExtra("types", types);
                    intent.putExtra("latitude", latitude);
                    intent.putExtra("longitude", longitude);

                    for (int i=0; i< reviewArray.length(); i++) {
                        JSONObject reviewObject = reviewArray.getJSONObject(i);
                        String authorName = reviewObject.getString("author_name");
                        String text = reviewObject.getString("text");

                        intent.putExtra("authorName"+i, authorName);
                        intent.putExtra("text"+i, text);
                    }

                    startActivity(intent);
                    finish();

                    System.out.println("성공");


                } catch (JSONException e) {
                    e.printStackTrace();//
                    Toast.makeText(getApplicationContext(), "Server Error", Toast.LENGTH_LONG).show();
                    System.out.println("server error : " + response);

                }
                //Log.i("VOLLEY", response);
            }
        },//통신 실패시
                new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Toast.makeText(getApplicationContext(), String.valueOf(error), Toast.LENGTH_SHORT).show();
                        System.out.println("에러 : " + String.valueOf(error));

                        //Log.v("VOLLEY", String.valueOf(error));
                    }
                }) {


            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }

            @Override
            public byte[] getBody() throws AuthFailureError {
                try {
                    return savedata == null ? null : savedata.getBytes("utf-8");
                } catch (UnsupportedEncodingException uee) {
                    //Log.v("Unsupported Encoding while trying to get the bytes", data);
                    return null;
                }
            }

        };
        requestQueue.add(stringRequest);
    }
}
