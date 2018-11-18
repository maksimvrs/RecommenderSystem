__all__ = []

from selector.main import app, learn

if __name__ == '__main__':
    learn()
    app.run(host='0.0.0.0', port=5000, debug=True)
