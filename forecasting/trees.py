import numpy as np
import matplotlib.pyplot as plt
import xgboost as xgb

from sklearn.metrics import mean_squared_error


def train(X_train: np.ndarray, X_test: np.ndarray, y_train: np.ndarray, y_test: np.ndarray) -> np.ndarray:
    train_dmatrix = xgb.DMatrix(X_train, label=y_train)
    test_dmatrix = xgb.DMatrix(X_test, label=y_test)

    params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse',
        'max_depth': 3,
        'eta': 0.1,
    }

    xgb_model = xgb.train(params, train_dmatrix, num_boost_round=100, evals=[(test_dmatrix, 'test')], early_stopping_rounds=10)

    y_pred = xgb_model.predict(test_dmatrix)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"Test RMSE: {rmse}")

    # plt.figure(figsize=(10, 5))
    # plt.plot(np.array([i for i in range(len(y_test))]), y_test, label="Actual")
    # plt.plot(np.array([i for i in range(len(y_test))]), y_pred, label="Predicted")
    # plt.legend()
    # plt.title("Actual vs Predicted Time Series Values")
    # plt.show()

    return y_pred
