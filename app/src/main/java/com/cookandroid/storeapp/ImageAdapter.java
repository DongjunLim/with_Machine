package com.cookandroid.storeapp;

import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.bumptech.glide.Glide;

import androidx.annotation.NonNull;
import androidx.viewpager.widget.PagerAdapter;

import static com.cookandroid.storeapp.InfoActivity.iContext;
import static com.cookandroid.storeapp.VisionServerActivity.place_id;

public class ImageAdapter extends PagerAdapter {
    private LayoutInflater inflater;
    private Context context;

    public ImageAdapter(Context context){
        this.context=context;
    }

    @Override
    public boolean isViewFromObject(@NonNull View view, @NonNull Object object) {
        return view==((LinearLayout)object);
    }

    @NonNull
    //viewPager를 넘기면 서버에서 매장에 해당하는 사진을 받아옴
    @Override
    public Object instantiateItem(@NonNull ViewGroup container, int position) {
        inflater = (LayoutInflater)context.getSystemService
                (Context.LAYOUT_INFLATER_SERVICE);
        View v = inflater.inflate(R.layout.slider, container, false);
        ImageView imageView=(ImageView)v.findViewById(R.id.imageView);
        String imageUrl="http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/picture/";
        String final_imageUrl=imageUrl+place_id+"/"+position+".jpg";
        //Glide 라이브러리를 사용하여 ImageView에 String형으로 저장한 imageUrl로 이미지를 로드
        Glide.with(this.context).load(final_imageUrl).fitCenter().error(R.drawable.noimage).into(imageView);
        final int pos=position;
        imageView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String imageUrl="http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/picture/";
                String final_imageUrl=imageUrl+place_id+"/"+pos+".jpg";

                Intent intent=new Intent().setClass(context,FullScreen.class);
                intent.putExtra("text",final_imageUrl);
                context.startActivity(intent);

            }
        });
        container.addView(v);

        return  v;

    }

    @Override
    public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
        container.invalidate();
    }

    @Override
    public int getCount() {
        return 5;
    }

}
