package com.cookandroid.storeapp;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;

import com.bumptech.glide.Glide;

import androidx.annotation.NonNull;
import androidx.viewpager.widget.PagerAdapter;

import static com.cookandroid.storeapp.VisionServerActivity.place_id;

public class ImageAdapter extends PagerAdapter {
    private int [] images={R.drawable.img2,R.drawable.img3,R.drawable.img4};
    private LayoutInflater inflater;
    private Context context;

    public ImageAdapter(Context context){
        this.context=context;
    }

    @Override
    public int getCount() {
        return images.length;
    }

    @Override
    public boolean isViewFromObject(@NonNull View view, @NonNull Object object) {
        return view==((LinearLayout)object);
    }

    @NonNull
    @Override
    public Object instantiateItem(@NonNull ViewGroup container, int position) {
        inflater = (LayoutInflater)context.getSystemService
                (Context.LAYOUT_INFLATER_SERVICE);
        View v = inflater.inflate(R.layout.slider, container, false);
        ImageView imageView=(ImageView)v.findViewById(R.id.imageView);
        //TextView textView=(TextView)v.findViewById(R.id.textView);

        String imageUrl="http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/picture/";

        Glide.with(this.context).load(imageUrl+place_id+"/0.jpg").into(imageView);
        //imageView.setImageResource(images[position]);

        //String text=(position + 1) +"번째 이미지";
        //textView.setText(text);
        container.addView(v);
        return  v;
    }

    @Override
    public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
        container.invalidate();
    }
}