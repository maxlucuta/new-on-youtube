import { createContext, Dispatch, SetStateAction } from "react";

type RootContextType = {
    SERVER_URL: string;
    updateUser: (n: string) => void;
    user: string;
};

export const RootContext = createContext<RootContextType>({
    SERVER_URL: "",
    updateUser: (n: string) => {},
    user: "",
});
