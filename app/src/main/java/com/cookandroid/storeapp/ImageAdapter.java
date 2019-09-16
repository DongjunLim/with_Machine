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
    static int page_count=1;
    private int [] images={};
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
    @Override
    public Object instantiateItem(@NonNull ViewGroup container, int position) {
        inflater = (LayoutInflater)context.getSystemService
                (Context.LAYOUT_INFLATER_SERVICE);
        View v = inflater.inflate(R.layout.slider, container, false);
        ImageView imageView=(ImageView)v.findViewById(R.id.imageView);
        String imageUrl="http://ec2-13-209-65-3.ap-northeast-2.compute.amazonaws.com/picture/";
        String final_imageUrl=imageUrl+place_id+"/"+position+".jpg";
        Glide.with(this.context).load(final_imageUrl).into(imageView);
        if(final_imageUrl.equals("")){
            imageView.setImageResource(R.drawable.img3);

            System.out.println("뒷사진없음 "+final_imageUrl);
        }


        container.addView(v);

        System.out.println("페이지 개수 : "+page_count);


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
