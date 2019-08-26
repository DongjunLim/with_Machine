package com.cookandroid.storeapp;

import android.content.Intent;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.api.client.extensions.android.http.AndroidHttp;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.gson.GsonFactory;
import com.google.api.services.vision.v1.Vision;
import com.google.api.services.vision.v1.VisionRequestInitializer;
import com.google.api.services.vision.v1.model.AnnotateImageRequest;
import com.google.api.services.vision.v1.model.BatchAnnotateImagesRequest;
import com.google.api.services.vision.v1.model.BatchAnnotateImagesResponse;
import com.google.api.services.vision.v1.model.EntityAnnotation;
import com.google.api.services.vision.v1.model.Feature;
import com.google.api.services.vision.v1.model.Image;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;

import androidx.appcompat.app.AppCompatActivity;

public class VisionServerActivity extends AppCompatActivity {
    private RequestQueue requestQueue;
    String api_key = BuildConfig.API_KEY;  //추가
    private final String TAG = VisionServerActivity.this.getClass().getSimpleName();
    private Uri uri;
    private String lang, country;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.wait);
        uri = ((CameraActivity)CameraActivity.cContext).photoUri;
        lang = ((StartActivity)StartActivity.mContext).lang;
        country = ((StartActivity)StartActivity.mContext).country;

        try {
            // scale the image to save on bandwidth
            Bitmap bitmap =
                    scaleBitmapDown(
                            MediaStore.Images.Media.getBitmap(getContentResolver(), uri),
                            1200);

            callCloudVision(bitmap);
        } catch (IOException e) {
            Log.d(TAG, "Image picking failed because " + e.getMessage());
        }
    }

    // Vision API
    private void callCloudVision(final Bitmap bitmap) {
        new AsyncTask<Object, Void, String>() {
            @Override
            protected String doInBackground(Object... params) {
                try {
                    HttpTransport httpTransport = AndroidHttp.newCompatibleTransport();
                    JsonFactory jsonFactory = GsonFactory.getDefaultInstance();

                    //Instantiate Vision
                    Vision.Builder builder = new Vision.Builder(httpTransport, jsonFactory, null);
                    builder.setVisionRequestInitializer(new VisionRequestInitializer(api_key));
                    Vision vision = builder.build();

                    BatchAnnotateImagesRequest batchAnnotateImagesRequest = new BatchAnnotateImagesRequest();
                    batchAnnotateImagesRequest.setRequests(new ArrayList<AnnotateImageRequest>() {{
                        AnnotateImageRequest annotateImageRequest = new AnnotateImageRequest();

                        Image base64EncodedImage = new Image();

                        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                        bitmap.compress(Bitmap.CompressFormat.JPEG, 90, byteArrayOutputStream);
                        byte[] imageBytes = byteArrayOutputStream.toByteArray();

                        base64EncodedImage.encodeContent(imageBytes);
                        annotateImageRequest.setImage(base64EncodedImage);

                        annotateImageRequest.setFeatures(new ArrayList<Feature>() {{
                            Feature labelDetection = new Feature();
                            labelDetection.setType("TEXT_DETECTION");
                            labelDetection.setMaxResults(10);
                            add(labelDetection);
                        }});

                        add(annotateImageRequest);

                    }});

                    Vision.Images.Annotate annotateRequest = vision.images().annotate(batchAnnotateImagesRequest);
                    annotateRequest.setDisableGZipContent(true);

                    BatchAnnotateImagesResponse response = annotateRequest.execute();

                    return convertResponseToString(response);

                } catch (IOException e) {
                    Log.e(TAG, "failed to make API request because " + e.toString());
                }

                return null;
            }

            @Override
            protected void onPostExecute(String response) {
                //super.onPostExecute(response);

                //Log.d(TAG, response);

                //result.setText("결과 : " + response);
                System.out.print("결과:"+response);
                nameMake(response);
            }
        }.execute();
    }

    public Bitmap scaleBitmapDown(Bitmap bitmap, int maxDimension) {

        int originalWidth = bitmap.getWidth();
        int originalHeight = bitmap.getHeight();
        int resizedWidth = maxDimension;
        int resizedHeight = maxDimension;

        if (originalHeight > originalWidth) {
            resizedHeight = maxDimension;
            resizedWidth = (int) (resizedHeight * (float) originalWidth / (float) originalHeight);
        } else if (originalWidth > originalHeight) {
            resizedWidth = maxDimension;
            resizedHeight = (int) (resizedWidth * (float) originalHeight / (float) originalWidth);
        } else if (originalHeight == originalWidth) {
            resizedHeight = maxDimension;
            resizedWidth = maxDimension;
        }
        return Bitmap.createScaledBitmap(bitmap, resizedWidth, resizedHeight, false);
    }
    private static String convertResponseToString(BatchAnnotateImagesResponse response) {
        String message = "I found these things:\n\n";

        List<EntityAnnotation> labels = response.getResponses().get(0).getTextAnnotations();
        if (labels != null) {
            message  = labels.get(0).getDescription();
        } else {
            message = "nothing";
        }

        return message;
    }


    //서버 연동
    public void nameMake(String response) {
        String re_response = response.toLowerCase();
        re_response = re_response.replace("\n", "").replace("\r", "");
        double num1 = 37.56621;
        double num2 = 126.9779;

        String data = "{"+
                "\"user_language\"" + ": "+"\"" + lang + "\","+"\n"+
                "\"visit_language\"" + ": "+"\"" + country + "\","+"\n"+
                "\"store_name\"" + ": "+"\"" + re_response + "\","+"\n"+
                "\"gps_lat\"" + ":" + num1 + ","+
                "\"gps_lon\"" + ":" + num2 +
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
                    String result = object.getString("result");
                    JSONObject subObject = new JSONObject(result);

                    // result 바로 밑 태그들
                    String address= subObject.getString("formatted_address");
                    String storeName = subObject.getString("name");
                    Double price = subObject.getDouble("price_level");
                    Double ratingBar = subObject.getDouble("rating");
                    String phoneNum = subObject.getString("international_phone_number");

                    // result의 reviews 태그 안 내용들
                    String reviews = subObject.getString("reviews");
                    JSONArray reviewArray = new JSONArray(reviews);

                    Intent intent = new Intent(getApplicationContext(), InfoActivity.class);
                    intent.putExtra("name", storeName);
                    System.out.println("매장이름:"+storeName);
                    intent.putExtra("address", address);
                    intent.putExtra("price", price);
                    intent.putExtra("ratingBar", ratingBar);
                    intent.putExtra("phoneNum", phoneNum);

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
