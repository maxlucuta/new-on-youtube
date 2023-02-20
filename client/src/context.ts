import { createContext, Dispatch, SetStateAction } from "react";

type RootContextType = {
    SERVER_URL: string;
    setToken: (n: string) => void;
    token: string;
};

export const RootContext = createContext<RootContextType>({
    SERVER_URL: "",
    setToken: (n: string) => {},
    token: "",
});
