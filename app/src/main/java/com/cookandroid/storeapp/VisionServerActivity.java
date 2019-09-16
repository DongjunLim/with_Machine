package com.cookandroid.storeapp;

import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
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
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import static com.android.volley.DefaultRetryPolicy.DEFAULT_TIMEOUT_MS;

public class VisionServerActivity extends AppCompatActivity {
    private RequestQueue requestQueue;
    String api_key = BuildConfig.API_KEY;  //추가
    private final String TAG = VisionServerActivity.this.getClass().getSimpleName();
    private Uri uri;
    private String lang, country;
    public double longitude, latitude;
    public static Context vContext;
    public static String place_id;
    ImageView gifView;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        setContentView(R.layout.wait);
        vContext = this;
        uri = ((CameraActivity)CameraActivity.cContext).photoUri;
        lang = ((StartActivity)StartActivity.mContext).lang;
        country = ((StartActivity)StartActivity.mContext).country;
        gifView = (ImageView)findViewById(R.id.gifView);
        Glide.with(this).load(R.drawable.giphy).into(gifView);

        try {
            if ( Build.VERSION.SDK_INT >= 23 &&
                    ContextCompat.checkSelfPermission( getApplicationContext(), android.Manifest.permission.ACCESS_FINE_LOCATION ) != PackageManager.PERMISSION_GRANTED ) {
                ActivityCompat.requestPermissions( VisionServerActivity.this, new String[] {  android.Manifest.permission.ACCESS_FINE_LOCATION  },
                        0 );
            }
            else{
                Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                String provider = location.getProvider();
                longitude = location.getLongitude();
                latitude = location.getLatitude();
                double altitude = location.getAltitude();

                lm.requestLocationUpdates(LocationManager.GPS_PROVIDER,
                        1000,
                        0,
                        gpsLocationListener);
                lm.requestLocationUpdates(LocationManager.NETWORK_PROVIDER,
                        1000,
                        0,
                        gpsLocationListener);
            }

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

    final LocationListener gpsLocationListener = new LocationListener() {
        public void onLocationChanged(Location location) {

            String provider = location.getProvider();
            longitude = location.getLongitude();
            latitude = location.getLatitude();
            double altitude = location.getAltitude();

        }

        public void onStatusChanged(String provider, int status, Bundle extras) {
        }

        public void onProviderEnabled(String provider) {
        }

        public void onProviderDisabled(String provider) {
        }
    };

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
    public void nameMake(String response) {
        String re_response = response.toLowerCase();
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

    public void Submit(String data) {
        final String savedata = data;
        String URL = "http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/data";

        requestQueue = Volley.newRequestQueue(getApplicationContext());
        StringRequest stringRequest = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
            //통신 성공 시
            @Override
            public void onResponse(String response) {
                // json 파싱

                try{
                    JSONObject object = new JSONObject(response);
                    String address= object.getString("formatted_address");
                    String storeName = object.getString("name");
                    Double price = object.getDouble("price_level");
                    Double ratingBar = object.getDouble("rating");
                    String phoneNum = object.getString("phone");
                    String types =  object.getString("types");
                    place_id = object.getString("place_id");

                    System.out.println("place_id : "+place_id);

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
                })

        {

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
        stringRequest.setRetryPolicy(new DefaultRetryPolicy(0, DefaultRetryPolicy.DEFAULT_MAX_RETRIES, DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        requestQueue.add(stringRequest);
    }
}
