package com.example.administrator.carapplication;

import android.os.Environment;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class DataSave {
    private static String path = Environment.getExternalStorageDirectory() + "/cardata/";
    private static boolean fos_open_flag_car = false;
    private static boolean fos_open_flag_lte = false;
    private static boolean fos_open_flag_sen = false;
    private FileOutputStream foscar = null;
    private FileOutputStream foslte = null;
    private FileOutputStream fossen = null;
    private SimpleDateFormat sdfNow1 = new SimpleDateFormat("MMdd_HHmmss");
    long carnow=0;
    long ltenow=0;
    long sennow=0;
    void cardata_save(String data) {
        String temp = "";
        if (!fos_open_flag_car) {//new file
            carnow = System.currentTimeMillis();
            String strNow = sdfNow1.format(new Date(carnow));
            File file_sen = new File(path + strNow + "_cardata.txt");
            try {
                foscar = new FileOutputStream(file_sen);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            fos_open_flag_car = true;
        }
        try {
            carnow = System.nanoTime();
            temp = carnow+""+"\t";
            foscar.write(temp.getBytes());
            foscar.write(data.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    void ltedata_save(String lte_info, double lat, double longi, double hei) {
        String temp = "";
        String data = "";
        data += lte_info + "\t" + lat + "\t" + longi + "\t" + hei + "\n";
        if (!fos_open_flag_lte) {//new file
            ltenow = System.currentTimeMillis();
            String strNow = sdfNow1.format(new Date(ltenow));
            File file_sen = new File(path + strNow + "_ltedata.txt");
            try {
                foslte = new FileOutputStream(file_sen);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            fos_open_flag_lte = true;
        }
        try {
            ltenow = System.nanoTime();
            temp = ltenow+""+"\t";
            foslte.write(temp.getBytes());
            foslte.write(data.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }

    }

    void sendata_save(float acc1, float acc2, float acc3, float gyro1, float gyro2, float gyro3, float m_field1, float m_field2, float m_field3, float pre) {
        String temp = "";
        String data = "";
        data += acc1 + "\t" + acc2 + "\t" + acc3 + "\t" + gyro1 + "\t" + gyro2 + "\t" + gyro3 + "\t" + m_field1 + "\t" + m_field2 + "\t" + m_field3 + "\t" + pre + "\n";

        if (!fos_open_flag_sen) {//new file
            sennow= System.currentTimeMillis();
            String strNow = sdfNow1.format(new Date(sennow));
            File file_sen = new File(path + strNow + "_sendata.txt");
            try {
                fossen = new FileOutputStream(file_sen);
            } catch (FileNotFoundException e) {
                e.printStackTrace();
            }
            fos_open_flag_sen = true;
        }
        try {
            sennow = System.nanoTime();
            temp = sennow+""+"\t";
            fossen.write(temp.getBytes());
            fossen.write(data.getBytes());
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
