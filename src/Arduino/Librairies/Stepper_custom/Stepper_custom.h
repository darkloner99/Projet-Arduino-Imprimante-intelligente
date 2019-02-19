
class Stepper_custom
{
    public:
        Stepper_custom(int dir, int pas);
        void onestep(int direction);
        void steps(int direction, int steps);
        void setspeed(int speed);

    private:
        int _dir;
        int _pas;
        int _speed;
};