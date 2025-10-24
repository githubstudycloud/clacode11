package com.example.common;

/**
 * 公共工具类
 * 这个类可能会使用lib目录中的第三方jar包
 */
public class CommonUtil {

    /**
     * 示例方法
     */
    public static String getMessage() {
        return "Hello from Common Module!";
    }

    /**
     * 格式化字符串
     * 如果需要使用lib中的jar，可以在这里调用
     */
    public static String formatMessage(String message) {
        // 示例：如果lib中有commons-lang3.jar，可以这样使用：
        // return StringUtils.capitalize(message);

        // 现在先用简单实现
        if (message == null || message.isEmpty()) {
            return "";
        }
        return message.substring(0, 1).toUpperCase() + message.substring(1);
    }
}
