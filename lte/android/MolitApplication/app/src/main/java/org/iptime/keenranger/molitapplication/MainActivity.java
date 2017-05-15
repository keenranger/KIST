package org.iptime.keenranger.molitapplication;

import android.app.Activity;
import android.graphics.Color;
import android.os.CountDownTimer;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.os.Bundle;

import android.util.Log;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;


public class MainActivity extends Activity {

    TextView tv;
    ImageView aaaImage = null;
    ImageView bbbImage = null;
    ImageView cccImage = null;
    ImageView dddImage = null;
    TextView aaaText = null;
    TextView bbbText = null;
    TextView cccText = null;
    TextView dddText = null;
    CountDownTimer aaaImageTimer = null;
    CountDownTimer bbbImageTimer = null;
    CountDownTimer cccImageTimer = null;
    CountDownTimer dddImageTimer = null;
    CountDownTimer aaaTextTimer = null;
    CountDownTimer bbbTextTimer = null;
    CountDownTimer cccTextTimer = null;
    CountDownTimer dddTextTimer = null;
    //  TCP연결 관련
    private Socket clientSocket;
    private BufferedReader socketIn;
    // private PrintWriter socketOut;
    private int port = 6000;
    private final String ip = "192.168.0.200";
    private Thread recvThread;
    private Thread checkThread;
    Handler CheckHandler;

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);
        tv = (TextView) findViewById(R.id.tv);

        aaaImage = (ImageView) findViewById(R.id.topImage);
        bbbImage = (ImageView) findViewById(R.id.leftImage);
        cccImage = (ImageView) findViewById(R.id.bottomImage);
        dddImage = (ImageView) findViewById(R.id.rightImage);
        aaaText = (TextView) findViewById(R.id.topText);
        bbbText = (TextView) findViewById(R.id.leftText);
        cccText = (TextView) findViewById(R.id.bottomText);
        dddText = (TextView) findViewById(R.id.rightText);


        aaaImage.setImageResource(R.drawable.black);
        bbbImage.setImageResource(R.drawable.black);
        cccImage.setImageResource(R.drawable.black);
        dddImage.setImageResource(R.drawable.black);
        aaaText.setText("0");
        bbbText.setText("0");
        cccText.setText("0");
        dddText.setText("0");

        CheckHandler = new Handler();

        try {
            clientSocket = new Socket(ip, port);
            socketIn = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            //socketOut = new PrintWriter(clientSocket.getOutputStream(), true);
        } catch (Exception e) {
            e.printStackTrace();
        }
        MessageThread();
        CheckThread();
        //socketOut.println(123);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        try {
            clientSocket.close();
            socketIn.close();
            recvThread.interrupt();
            checkThread.interrupt();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    void MessageThread() {
        recvThread = new Thread(new Runnable() {
            public void run() {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        String data = socketIn.readLine();
                        Message msg = handler.obtainMessage();
                        msg.obj = data;
                        handler.sendMessage(msg);
                    } catch (Exception e) {
                        Toast.makeText(getApplicationContext(), "Message Thread failure.", Toast.LENGTH_LONG).show();
                        finish();            // App 종료.
                    }
                }
            }
        });
        recvThread.start();
    }

    void CheckThread() {
        checkThread = new Thread(new Runnable() {
            public void run() {
                try {
                    String max = "none";
                    double num=0.;
                    double temp;
                    temp=Float.parseFloat(aaaText.getText().toString());
                    if (temp > num) {
                        max = "aaa";
                        num=temp;
                    }
                    temp=Float.parseFloat(bbbText.getText().toString());
                    if (Float.parseFloat(bbbText.getText().toString()) > num) {
                        max = "bbb";
                        num=temp;
                    }
                    temp=Float.parseFloat(cccText.getText().toString());
                    if (Float.parseFloat(cccText.getText().toString()) > num) {
                        max = "ccc";
                        num=temp;
                    }
                    if (Float.parseFloat(dddText.getText().toString()) > num) {
                        max = "ddd";
                    }
                    switch (max) {
                        case "aaa":
                            CheckHandler.post(new Runnable() {
                                public void run() {
                                    aaaText.setBackgroundColor(Color.parseColor("#d50000"));
                                    bbbText.setBackgroundColor(0x000000);
                                    cccText.setBackgroundColor(0x000000);
                                    dddText.setBackgroundColor(0x000000);
                                }
                            });
                            break;
                        case "bbb":
                            CheckHandler.post(new Runnable() {
                                public void run() {
                                    aaaText.setBackgroundColor(0x000000);
                                    bbbText.setBackgroundColor(Color.parseColor("#d50000"));
                                    cccText.setBackgroundColor(0x000000);
                                    dddText.setBackgroundColor(0x000000);
                                }
                            });
                            break;
                        case "ccc":
                            CheckHandler.post(new Runnable() {
                                public void run() {
                                    aaaText.setBackgroundColor(0x000000);
                                    bbbText.setBackgroundColor(0x000000);
                                    cccText.setBackgroundColor(Color.parseColor("#d50000"));
                                    dddText.setBackgroundColor(0x000000);
                                }
                            });
                            break;
                        case "ddd":
                            CheckHandler.post(new Runnable() {
                                public void run() {
                                    aaaText.setBackgroundColor(0x000000);
                                    bbbText.setBackgroundColor(0x000000);
                                    cccText.setBackgroundColor(0x000000);
                                    dddText.setBackgroundColor(Color.parseColor("#d50000"));
                                }
                            });
                            break;
                        default:
                            CheckHandler.post(new Runnable() {
                                public void run() {
                                    aaaText.setBackgroundColor(0x000000);
                                    bbbText.setBackgroundColor(0x000000);
                                    cccText.setBackgroundColor(0x000000);
                                    dddText.setBackgroundColor(0x000000);
                                }
                            });
                            break;
                    }
                } catch (Exception e) {
                    Toast.makeText(getApplicationContext(), "Check Thread failure.", Toast.LENGTH_LONG).show();
                    finish();            // App 종료.
                }

            }
        });
        checkThread.start();
    }


    Handler handler = new Handler() {//message
        @Override
        public void handleMessage(Message msg) {
            super.handleMessage(msg);
            String[] arr = msg.obj.toString().split("]");
            switch (arr[1]) {
                case "Shaking!":
                    switch (arr[0]) {
                        case "[AAA":
                            aaaImage.setImageResource(R.drawable.red);
                            if (aaaImageTimer != null) {
                                aaaImageTimer.cancel();
                            }
                            aaaImageTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    aaaImage.setImageResource(R.drawable.green);
                                }
                            };
                            aaaImageTimer.start();
                            break;
                        case "[BBB":
                            bbbImage.setImageResource(R.drawable.red);
                            if (bbbImageTimer != null) {
                                bbbImageTimer.cancel();
                            }
                            bbbImageTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    bbbImage.setImageResource(R.drawable.green);
                                }
                            };
                            bbbImageTimer.start();
                            break;
                        case "[CCC":
                            cccImage.setImageResource(R.drawable.red);
                            if (cccImageTimer != null) {
                                cccImageTimer.cancel();
                            }
                            cccImageTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    cccImage.setImageResource(R.drawable.green);
                                }
                            };
                            cccImageTimer.start();
                            break;
                        case "[DDD":
                            dddImage.setImageResource(R.drawable.red);
                            if (dddImageTimer != null) {
                                dddImageTimer.cancel();
                            }
                            dddImageTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    dddImage.setImageResource(R.drawable.green);
                                }
                            };
                            dddImageTimer.start();
                            break;
                    }
                    break;
                case "attached":
                    switch (arr[0]) {
                        case "[AAA":
                            aaaImage.setImageResource(R.drawable.green);
                            break;
                        case "[BBB":
                            bbbImage.setImageResource(R.drawable.green);
                            break;
                        case "[CCC":
                            cccImage.setImageResource(R.drawable.green);
                            break;
                        case "[DDD":
                            dddImage.setImageResource(R.drawable.green);
                            break;
                    }
                    break;
                case "Noise!":
                    switch (arr[0]) {
                        case "[AAA":
                            aaaText.setText(arr[2]);
                            CheckThread();
                            if (aaaTextTimer != null) {
                                aaaTextTimer.cancel();
                            }
                            aaaTextTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    aaaText.setText("0");
                                    CheckThread();
                                }
                            };
                            aaaTextTimer.start();
                            break;
                        case "[BBB":
                            bbbText.setText(arr[2]);
                            CheckThread();
                            if (bbbTextTimer != null) {
                                bbbTextTimer.cancel();
                            }
                            bbbTextTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    bbbText.setText("0");
                                    CheckThread();
                                }
                            };
                            bbbTextTimer.start();
                            break;
                        case "[CCC":
                            cccText.setText(arr[2]);
                            CheckThread();
                            if (cccTextTimer != null) {
                                cccTextTimer.cancel();
                            }
                            cccTextTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    cccText.setText("0");
                                    CheckThread();
                                }
                            };
                            cccTextTimer.start();
                            break;
                        case "[DDD":
                            dddText.setText(arr[2]);
                            CheckThread();
                            if (dddTextTimer != null) {
                                dddTextTimer.cancel();
                            }
                            dddTextTimer = new CountDownTimer(3000, 100) {
                                public void onTick(long millisUntilFinished) {
                                }

                                public void onFinish() {
                                    dddText.setText("0");
                                    CheckThread();
                                }
                            };
                            dddTextTimer.start();
                            break;
                    }
                    break;

            }

        }
    };
}