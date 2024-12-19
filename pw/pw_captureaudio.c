/* PipeWire */
/* SPDX-FileCopyrightText: Copyright © 2022 Wim Taymans */
/* SPDX-License-Identifier: MIT */

/*
 [title]
 Audio capture using \ref pw_stream "pw_stream".
 [title]
 */

#include <stdio.h>
#include <errno.h>
#include <math.h>
#include <signal.h>
#include <string.h>

#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

#include <spa/param/audio/format-utils.h>

#include <pipewire/pipewire.h>
#include <fftw3.h>

#define SAMPLE_RATE 48000

struct histogramCell
{
    int count;
    float sum;
};

/*int serial_write(int serialPort, void *data, size_t size)
{
    return 0;
}*/

struct data
{
    struct pw_main_loop *loop;
    struct pw_stream *stream;

    struct spa_audio_info format;
    unsigned move : 1;
    int serialPort;
};

void processSamples(const float *samples, size_t size, struct data *data)
{
    // Allocate memory for input and output arrays
    fftw_complex *in, *out;
    fftw_plan plan_forward;

    in = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * size);
    out = (fftw_complex *)fftw_malloc(sizeof(fftw_complex) * size);

    for (size_t i = 0; i < size; i++)
    {
        in[i][0] = samples[i] * 0.5 * (1 - cos(2 * 3.14 * i / (size - 1)));
        in[i][1] = 0.0;
    }

    plan_forward = fftw_plan_dft_1d(size, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

    fftw_execute(plan_forward);

    // int *frequencies = malloc(sizeof(unsigned int) * size);
    // int *amplitudes = malloc(sizeof(unsigned int) * size);
    int breakpointCount = 15; // n
    int *frequencyBreakpoints = malloc(sizeof(int) * breakpointCount);
    struct histogramCell *histogram = malloc(sizeof(struct histogramCell) * breakpointCount);
    for (int k = 0; k < breakpointCount; k++)
    {
        histogram[k].count = 0;
        histogram[k].sum = 0.0f;

        frequencyBreakpoints[k] = pow(10, 1.8 + (((float)k / (float)breakpointCount) * 2.75));
        // frequencyBreakpoints[k] = exp(3.9 + (((float)k / (float)breakpointCount) * 6.3));
    }

    frequencyBreakpoints[breakpointCount - 1] = 20000;
    histogram[breakpointCount - 1].count = 0;
    histogram[breakpointCount - 1].sum = 0.0f;

    // fprintf(stdout, "%c[%dA", 0x1b, 9 + 1);

    fprintf(stdout, "Forward FFT:\n");
    for (int i = 1; i < (size); i++)
    {
        int freq = (i * SAMPLE_RATE) / (size / 2);
        if (freq > 20000)
            continue;
        float amplitude = log10(sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1]) + 1); //  + out[i][1] * out[i][1]

        int histogramId = 8;
        for (int j = 0; j < breakpointCount; j++)
        {
            if (freq < frequencyBreakpoints[j])
            {
                histogramId = j;
                break;
            }
        }

        histogram[histogramId].count++;
        histogram[histogramId].sum += amplitude;

        // frequencies[i] = (i * 44100) / 1024;
        // amplitudes[i] = sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1]);
        //  printf("Frequency: %d, Amplitude: %f\n", (i * 44100) / 1024, sqrt(out[i][0] * out[i][0] + out[i][1] * out[i][1]));
        //  printf("out[%d] = %f + %fi\n", i, out[i][0], out[i][1]);
    }

    char *stripData = malloc(breakpointCount);

    for (size_t i = 0; i < breakpointCount; i++)
    {
        int frequency = frequencyBreakpoints[i];
        float amplitude = histogram[i].sum / histogram[i].count;
        char *bar = malloc(21);
        memset(bar, ' ', 20);
        bar[0] = '|';
        bar[19] = '|';
        bar[20] = 0;
        int bar_count = round((20 / 3) * amplitude);
        for (int j = 1; j < bar_count; j++)
        {
            bar[j] = '#';
        }
        fprintf(stdout, "Frequency: %5dHz, Amplitude: %2.2f %s\n", frequencyBreakpoints[i], amplitude, bar);
        // char buf[1] = {((255 / 3) * amplitude)};
        stripData[i] = (255 / 3) * amplitude;
        // write(data->serialPort, buf, 1);
        free(bar);
    }

    write(data->serialPort, stripData, breakpointCount);

    free(stripData);
    free(frequencyBreakpoints);
    free(histogram);

    fflush(stdout);

    fftw_destroy_plan(plan_forward);
    fftw_free(in);
    fftw_free(out);
}

/* our data processing function is in general:
 *
 *  struct pw_buffer *b;
 *  b = pw_stream_dequeue_buffer(stream);
 *
 *  .. consume stuff in the buffer ...
 *
 *  pw_stream_queue_buffer(stream, b);
 */
static void on_process(void *userdata)
{
    struct data *data = userdata;
    struct pw_buffer *b;
    struct spa_buffer *buf;
    float *samples, max;
    uint32_t c, n, n_channels, n_samples, peak;

    if ((b = pw_stream_dequeue_buffer(data->stream)) == NULL)
    {
        pw_log_warn("out of buffers: %m");
        return;
    }

    buf = b->buffer;
    if ((samples = buf->datas[0].data) == NULL)
        return;

    n_channels = data->format.info.raw.channels;
    n_samples = buf->datas[0].chunk->size / sizeof(float);

    /* move cursor up */
    if (data->move)
        fprintf(stdout, "%c[%dA", 0x1b, n_channels + 1);
    fprintf(stdout, "captured %d samples\n", n_samples / n_channels);
    for (c = 0; c < data->format.info.raw.channels; c++)
    {
        max = 0.0f;
        for (n = c; n < n_samples; n += n_channels)
            max = fmaxf(max, fabsf(samples[n]));

        peak = (uint32_t)SPA_CLAMPF(max * 30, 0.f, 39.f);

        fprintf(stdout, "channel %d: |%*s%*s| peak:%f\n",
                c, peak + 1, "*", 40 - peak, "", max);
    }
    data->move = true;
    fflush(stdout);

    processSamples(samples, n_samples, data);

    pw_stream_queue_buffer(data->stream, b);
}

/* Be notified when the stream param changes. We're only looking at the
 * format changes.
 */
static void
on_stream_param_changed(void *_data, uint32_t id, const struct spa_pod *param)
{
    struct data *data = _data;

    /* NULL means to clear the format */
    if (param == NULL || id != SPA_PARAM_Format)
        return;

    if (spa_format_parse(param, &data->format.media_type, &data->format.media_subtype) < 0)
        return;

    /* only accept raw audio */
    if (data->format.media_type != SPA_MEDIA_TYPE_audio ||
        data->format.media_subtype != SPA_MEDIA_SUBTYPE_raw)
        return;

    /* call a helper function to parse the format for us. */
    spa_format_audio_raw_parse(param, &data->format.info.raw);

    fprintf(stdout, "capturing rate:%d channels:%d\n",
            data->format.info.raw.rate, data->format.info.raw.channels);
}

static const struct pw_stream_events stream_events = {
    PW_VERSION_STREAM_EVENTS,
    .param_changed = on_stream_param_changed,
    .process = on_process,
};

static void do_quit(void *userdata, int signal_number)
{
    struct data *data = userdata;
    pw_main_loop_quit(data->loop);
}

int main(int argc, char *argv[])
{
    struct data data = {
        0,
    };
    const struct spa_pod *params[1];
    uint8_t buffer[2048];
    struct pw_properties *props;
    struct spa_pod_builder b = SPA_POD_BUILDER_INIT(buffer, sizeof(buffer));

    int serial_port = open("/dev/ttyACM0", O_RDWR);

    if (serial_port < 0)
    {
        printf("Error opening the serial port: %s\n", strerror(errno));
        return 1;
    }

    struct termios tty;

    // Get the current configuration of the serial port
    if (tcgetattr(serial_port, &tty) != 0)
    {
        printf("Error getting serial port attributes: %s\n", strerror(errno));
        return 1;
    }

    // Set Baud Rate
    cfsetispeed(&tty, B9600); // Input baud rate (9600 baud)
    cfsetospeed(&tty, B9600); // Output baud rate (9600 baud)

    // Set 8 data bits, no parity, 1 stop bit
    tty.c_cflag &= ~PARENB; // No parity
    tty.c_cflag &= ~CSTOPB; // 1 stop bit
    tty.c_cflag &= ~CSIZE;  // Mask the character size bits
    tty.c_cflag |= CS8;     // Set 8 data bits

    // Disable hardware flow control (RTS/CTS)
    // tty.c_cflag &= ~CRTSCTS;

    // Set local mode and enable receiver
    tty.c_cflag |= CREAD | CLOCAL;

    // Disable software flow control
    tty.c_iflag &= ~(IXON | IXOFF | IXANY);

    // Set raw input mode (disable canonical mode)
    tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);

    // Set raw output mode
    tty.c_oflag &= ~OPOST;

    // Set timeouts
    tty.c_cc[VTIME] = 1; // Timeout for read (in deciseconds)
    tty.c_cc[VMIN] = 1;  // Minimum number of characters to read

    // Apply the settings
    if (tcsetattr(serial_port, TCSANOW, &tty) != 0)
    {
        printf("Error setting serial port attributes: %s\n", strerror(errno));
        return 1;
    }

    int buf[1];
    int n = read(serial_port, buf, 1);
    if (n < 0)
    {
        printf("Error reading from serial port: %s\n", strerror(errno));
        return 1;
    }

    data.serialPort = serial_port;

    printf("Waiting for buffer to load\n");
    sleep(2);

    // Write data to serial port
    /*char msg[15] = {0xff, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee};
    n = write(serial_port, msg, 15);
    if (n < 0)
    {
        printf("Error writing to serial port: %s\n", strerror(errno));
        return 1;
    }*/

    pw_init(&argc, &argv);

    /* make a main loop. If you already have another main loop, you can add
     * the fd of this pipewire mainloop to it. */
    data.loop = pw_main_loop_new(NULL);

    pw_loop_add_signal(pw_main_loop_get_loop(data.loop), SIGINT, do_quit, &data);
    pw_loop_add_signal(pw_main_loop_get_loop(data.loop), SIGTERM, do_quit, &data);

    /* Create a simple stream, the simple stream manages the core and remote
     * objects for you if you don't need to deal with them.
     *
     * If you plan to autoconnect your stream, you need to provide at least
     * media, category and role properties.
     *
     * Pass your events and a user_data pointer as the last arguments. This
     * will inform you about the stream state. The most important event
     * you need to listen to is the process event where you need to produce
     * the data.
     */
    props = pw_properties_new(PW_KEY_MEDIA_TYPE, "Audio",
                              PW_KEY_CONFIG_NAME, "client-rt.conf",
                              PW_KEY_MEDIA_CATEGORY, "Monitor",
                              PW_KEY_MEDIA_ROLE, "Music",
                              PW_KEY_NODE_LATENCY, "2048/48000",
                              NULL);
    if (argc > 1)
        /* Set stream target if given on command line */
        pw_properties_set(props, PW_KEY_TARGET_OBJECT, argv[1]);

    /* uncomment if you want to capture from the sink monitor ports */
    pw_properties_set(props, PW_KEY_STREAM_CAPTURE_SINK, "true");

    data.stream = pw_stream_new_simple(
        pw_main_loop_get_loop(data.loop),
        "audio-capture",
        props,
        &stream_events,
        &data);

    /* Make one parameter with the supported formats. The SPA_PARAM_EnumFormat
     * id means that this is a format enumeration (of 1 value).
     * We leave the channels and rate empty to accept the native graph
     * rate and channels. */
    params[0] = spa_format_audio_raw_build(&b, SPA_PARAM_EnumFormat,
                                           &SPA_AUDIO_INFO_RAW_INIT(
                                                   .format = SPA_AUDIO_FORMAT_F32,
                                                   .rate = SAMPLE_RATE,
                                                   .channels = 2));

    /* Now connect this stream. We ask that our process function is
     * called in a realtime thread. */
    pw_stream_connect(data.stream,
                      PW_DIRECTION_INPUT,
                      PW_ID_ANY,
                      PW_STREAM_FLAG_AUTOCONNECT |
                          PW_STREAM_FLAG_MAP_BUFFERS |
                          PW_STREAM_FLAG_RT_PROCESS,
                      params, 1);

    /* and wait while we let things run */
    pw_main_loop_run(data.loop);

    pw_stream_destroy(data.stream);
    pw_main_loop_destroy(data.loop);
    pw_deinit();

    return 0;
}