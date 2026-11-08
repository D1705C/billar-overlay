package org.diego.billar;

import android.content.Context;
import android.graphics.*;
import android.view.MotionEvent;
import android.view.View;

public class OverlayView extends View {
    public interface Listener { void onToque(float x, float y); }

    private float[] lineas = new float[0];
    private int[] colores = new int[0];
    private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private Listener listener;
    private boolean visible = true;

    public OverlayView(Context c) {
        super(c);
        paint.setStrokeWidth(6f);
        paint.setStrokeCap(Paint.Cap.ROUND);
    }

    public void setListener(Listener l) { listener = l; }
    public void setVisibleLines(boolean v) { visible = v; postInvalidate(); }

    public void setLines(float[] l, int[] c) {
        lineas = l; colores = c; postInvalidate();
    }

    @Override protected void onDraw(Canvas canvas) {
        if (!visible) return;
        for (int i = 0; i < colores.length; i++) {
            paint.setColor(colores[i]);
            canvas.drawLine(lineas[i*4], lineas[i*4+1],
                            lineas[i*4+2], lineas[i*4+3], paint);
        }
    }

    @Override public boolean onTouchEvent(MotionEvent e) {
        if (e.getAction() == MotionEvent.ACTION_DOWN && listener != null)
            listener.onToque(e.getRawX(), e.getRawY());
        return true;
    }
}
