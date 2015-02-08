#include <Arduino.h>
#include <MeggyJrRGB/MeggyJrSimple.h>

const byte arrow_color = Orange;
const byte border_color = DimRed;

void clear_display()
{
    int i;

    ClearSlate();

    for (i = 0; i < 8; i++) {
        DrawPx(i, 0, border_color);
        DrawPx(0, i, border_color);
        DrawPx(i, 7, border_color);
        DrawPx(7, i, border_color);
    }
}

void setup()
{
    MeggyJrSimpleSetup();

    Serial.begin(9600);

    SetAuxLEDs(1); // turn on one LED to show the device is ON
    clear_display();
}

void loop()
{
    CheckButtonsPress();

    if (Button_Up) {
        Serial.println('w');

        clear_display();
        DrawPx(3, 1, arrow_color);
        DrawPx(3, 2, arrow_color);
        DrawPx(3, 3, arrow_color);
        DrawPx(3, 4, arrow_color);
        DrawPx(3, 5, arrow_color);
        DrawPx(3, 6, arrow_color);

        DrawPx(2, 5, arrow_color);
        DrawPx(1, 4, arrow_color);

        DrawPx(4, 5, arrow_color);
        DrawPx(5, 4, arrow_color);
    } else if (Button_Down) {
        clear_display();
    } else if (Button_Left) {
        Serial.println('a');

        clear_display();
        DrawPx(6, 3, arrow_color);
        DrawPx(5, 3, arrow_color);
        DrawPx(4, 3, arrow_color);
        DrawPx(3, 3, arrow_color);
        DrawPx(2, 3, arrow_color);
        DrawPx(1, 3, arrow_color);

        DrawPx(2, 4, arrow_color);
        DrawPx(3, 5, arrow_color);

        DrawPx(2, 2, arrow_color);
        DrawPx(3, 1, arrow_color);
    } else if (Button_Right) {
        Serial.println('d');

        clear_display();
        DrawPx(6, 3, arrow_color);
        DrawPx(5, 3, arrow_color);
        DrawPx(4, 3, arrow_color);
        DrawPx(3, 3, arrow_color);
        DrawPx(2, 3, arrow_color);
        DrawPx(1, 3, arrow_color);

        DrawPx(5, 4, arrow_color);
        DrawPx(4, 5, arrow_color);

        DrawPx(5, 2, arrow_color);
        DrawPx(4, 1, arrow_color);
    } else if (Button_A) {
        Serial.println('e');

        clear_display();
        DrawPx(6, 3, arrow_color);
        DrawPx(5, 3, arrow_color);
        DrawPx(4, 3, arrow_color);
        DrawPx(3, 3, arrow_color);
        DrawPx(2, 3, arrow_color);
        DrawPx(1, 3, arrow_color);
        DrawPx(1, 2, arrow_color);
        DrawPx(1, 1, arrow_color);

        DrawPx(5, 4, arrow_color);
        DrawPx(4, 5, arrow_color);

        DrawPx(5, 2, arrow_color);
        DrawPx(4, 1, arrow_color);
    } else if (Button_B) {
        Serial.println('q');

        clear_display();
        DrawPx(6, 1, arrow_color);
        DrawPx(6, 2, arrow_color);
        DrawPx(6, 3, arrow_color);
        DrawPx(5, 3, arrow_color);
        DrawPx(4, 3, arrow_color);
        DrawPx(3, 3, arrow_color);
        DrawPx(2, 3, arrow_color);
        DrawPx(1, 3, arrow_color);

        DrawPx(2, 4, arrow_color);
        DrawPx(3, 5, arrow_color);

        DrawPx(2, 2, arrow_color);
        DrawPx(3, 1, arrow_color);
    }

    DisplaySlate();
    delay(50);
}
